from django.shortcuts import render
from django.http import HttpResponse
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
    context = {'code': code}
    return render(request, 'program.html', context)

def about_view(request):
    return render(request, 'about.html',)