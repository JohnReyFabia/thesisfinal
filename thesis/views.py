from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index_view(request):
    return render(request, 'index.html',)

def college_view(request):
    return render(request, 'college.html',)
    
def program_view(request, program):
    context = {'program': program}
    return render(request, 'program.html', context)

def about_view(request):
    return render(request, 'about.html',)