from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import (
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