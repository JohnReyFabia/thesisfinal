from django.contrib import admin
from .models import (
    College, 
    Program, 
    CurriculumYear, 
    ProgramSlot, 
    )

# Register your models here.

admin.site.register(CurriculumYear)
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "college_name",)
    search_fields = ("id", "code", "college_name", )

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "college" ,"program_name", )
    search_fields = ("id", "college__college_name" ,"program_name",)
    

@admin.register(ProgramSlot)
class ProgramSlotAdmin(admin.ModelAdmin):
    list_display = ("id", "program", "year", "no_of_slot" )
    search_fields = ("id", "program_program_name" ,"year_year", "no_of_slot")
    

