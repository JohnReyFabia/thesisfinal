from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import (
    Prediction,
    ProcessedData,
    College,
    Program,
    ProgramSlot,
    CurriculumYear,
)

# Create your views here.

def index_view(request):
    return render(request, 'index.html',)

def college_view(request):
    return render(request, 'college.html',)
    
def program_view(request, code):
    
    selected_college = College.objects.get(code=code)
    print(f"Selected College: {selected_college}")

    college_programs = Program.objects.filter(college__college_name=selected_college)
    print(college_programs)
    
    context = {
        'code': code,
        'selected_college': selected_college,
        'college_programs': college_programs
        }
    
    return render(request, 'program.html', context)

def get_selected_program(request, code, program_name):
    selected_college = College.objects.filter(code=code).first()
    
    if not selected_college:
        return JsonResponse({'error': 'College not found'}, status=404)
    
    selected_program_slots = ProgramSlot.objects.filter(program__program_name=program_name, program__college=selected_college)

    if not selected_program_slots.exists():
        return JsonResponse({'error': 'Program not found'}, status=404)


    program_details = {
        'program_name': selected_program_slots.first().program.program_name, 
        'years': []
    }


    for program_slot in selected_program_slots:
        program_year_data = {
            'year': program_slot.year.year,  
            'no_of_slots': program_slot.no_of_slot  
        }
        
        program_details['years'].append(program_year_data)

    return JsonResponse(program_details)


    
def about_view(request):
    return render(request, 'about.html',)

from django.http import JsonResponse
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from .models import ProcessedData, ProgramSlot, Program, CurriculumYear, College

from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import numpy as np


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if file.content_type == 'text/csv':
            try:
                dataset = pd.read_csv(file)
                print("Columns in the dataset:", dataset.columns)

                # Remove any extra spaces from column names
                dataset.columns = dataset.columns.str.strip()
                print("Cleaned column names:", dataset.columns)

                # Ensure the 'Programs' column exists
                if 'PROGRAMS' not in dataset.columns:
                    raise ValueError("The dataset must contain a 'PROGRAMS' column.")

                # Convert 'Programs' column to string type
                dataset['PROGRAMS'] = dataset['PROGRAMS'].astype(str)

                # Ensure dataset has the necessary columns
                required_columns = ['S2_22-23', 'S2_20-21', 'S2_23-24', 'PROGRAMS', 'S2_21-22', 'S1_20-21', 'Year']
                missing_columns = [col for col in required_columns if col not in dataset.columns]
                if missing_columns:
                    raise ValueError(f"Uploaded file does not contain required columns: {missing_columns}")

                # Drop rows with missing target variable values
                dataset.dropna(subset=['S2_21-22'], inplace=True)
                print("Dropped rows with missing 'S2_21-22' values. Remaining data:", dataset.shape)

                # Split the data into features (X) and target (y)
                X = dataset[['S2_22-23', 'S2_20-21', 'S2_23-24']]
                y = dataset['S2_21-22']
                print("Features (X) shape:", X.shape)
                print("Target (y) shape:", y.shape)

                # Train the Random Forest Regressor
                regressor = RandomForestRegressor()
                regressor.fit(X, y)
                print("Random Forest Regressor trained successfully.")

                # Predict
                predictions = regressor.predict(X)
                print("Predictions:", predictions)

                # Calculate accuracy metrics 
                mse = mean_squared_error(y, predictions)
                r2 = r2_score(y, predictions) 
                print(f"Mean Squared Error: {mse}")
                print(f"R2 Score: {r2}")

                # Subtract S1_20-21 from the predictions, round to nearest whole number, and store in predicted_slots
                dataset['predicted_slots'] = (dataset['S1_20-21'] - predictions).round().astype(int)
                print("Predictions after subtraction and rounding:", dataset['predicted_slots'])

                # Ensure no null values in 'predicted_slots'
                dataset['predicted_slots'] = dataset['predicted_slots'].fillna(0)
                print("Checked for null values in 'predicted_slots':", dataset['predicted_slots'])

                # Print the entire dataset for debugging
                print("Dataset after adding predictions:\n", dataset.head())


                # Fetch existing programs and years from ProgramSlot
                program_slots = ProgramSlot.objects.all()
                program_data = program_slots.values('program__program_name', 'year__year').distinct()

                # Save the predictions to the database
                for _, row in dataset.iterrows():
                    program_name = row['PROGRAMS']
                    year_value = row['Year']

                    # Check if the program and year combination exists
                    existing_program_slots = program_data.filter(program__program_name=program_name, year__year=year_value)
                    if existing_program_slots.exists():
                        programs = Program.objects.filter(program_name=program_name)
                        year_instance = CurriculumYear.objects.get(year=year_value)

                        # Save to ProcessedData
                        ProcessedData.objects.create(
                            programs=row['PROGRAMS'],
                            year_20_21=row['S2_20-21'],
                            year_22_23=row['S2_22-23'],
                            year_23_24=row['S2_23-24'],
                            predicted_slots=row['predicted_slots']
                        )

                        # Update ProgramSlot for each matching program
                        for program_instance in programs:
                            program_slot_instance = ProgramSlot.objects.filter(program=program_instance, year=year_instance).first()
                            if program_slot_instance:
                                program_slot_instance.no_of_slot = row['predicted_slots']
                                program_slot_instance.save()
                                print(f"Updated ProgramSlot: Program: {program_slot_instance.program.program_name}, Year: {program_slot_instance.year.year}, No of Slots: {program_slot_instance.no_of_slot}")
                            else:
                                print(f"Error: No matching ProgramSlot found for Program: {row['PROGRAMS']} and Year: {row['Year']}")
                    else:
                        print(f"Error: No matching ProgramSlot found for Program: {program_name} and Year: {year_value}")

                print("Data saved to the database successfully.")

                # Convert the dataset to JSON and return it as a response
                response_data = dataset[['PROGRAMS', 'S2_22-23', 'S2_20-21', 'S2_23-24', 'predicted_slots']].to_dict(orient='records')
                return JsonResponse({'data': response_data}, safe=False)


        
            except ValueError as ve:
                print(f"ValueError: {ve}")
                return JsonResponse({'error': str(ve)}, status=400)
            except Exception as e:
                print(f"Exception: {e}")
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Invalid file type. Only CSV files are accepted.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def get_program_details(request, code, program_name):
    try:
        college = College.objects.get(code=code)
        program = Program.objects.get(program_name=program_name, college=college)
        program_slots = ProgramSlot.objects.filter(program=program).values('year__year', 'no_of_slot')
        
        data = {
            'program_name': program.program_name,
            'years': list(program_slots),
        }
        return JsonResponse(data)
    except College.DoesNotExist:
        return JsonResponse({'error': 'College not found'}, status=404)
    except Program.DoesNotExist:
        return JsonResponse({'error': 'Program not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def check_no_of_slot(request):
    program_slots = ProgramSlot.objects.filter(no_of_slot__isnull=False).values('program__program_name', 'year__year', 'no_of_slot')
    data = list(program_slots)
    return JsonResponse({'program_slots': data})


from django.http import JsonResponse
from .models import ProgramSlot, Program, CurriculumYear

def fetch_program_data(request):
    # Fetch all unique programs and their respective years from ProgramSlot
    program_slots = ProgramSlot.objects.all()
    program_data = program_slots.values('program__program_name', 'year__year').distinct()

    data = [{"program_name": item['program__program_name'], "year": item['year__year']} for item in program_data]
    return JsonResponse({'program_data': data})

