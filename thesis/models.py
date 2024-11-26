from django.db import models

# Create your models here.
class College(models.Model):
    code = models.CharField(max_length=5, default="None")
    college_name = models.CharField(max_length=55)
    
    def __str__(self):
        return f"{self.college_name}"

    class Meta:
        verbose_name_plural = "colleges"


class Program(models.Model):
    program_name = models.CharField(max_length=120)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.program_name}"

    class Meta:
        verbose_name_plural = "programs"
        

class CurriculumYear(models.Model):
    year = models.IntegerField(default=1)
    

    def __str__(self):
        return f"{self.year}"

    class Meta:
        verbose_name_plural = "Curriculum Years"
        

class ProgramSlot(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    year = models.ForeignKey(CurriculumYear, on_delete=models.CASCADE)
    no_of_slot = models.IntegerField(default=0)
    
    def _str_(self):
        return f"{self.program.program_name}"
    
    class Meta:
        verbose_name_plural = "Program Slots"

class ProcessedData(models.Model):
    programs = models.CharField(max_length=255)
    year_20_21 = models.FloatField()
    year_22_23 = models.FloatField()
    year_23_24 = models.FloatField()
    predicted_slots = models.FloatField()

    def __str__(self):
        return self.programs


class Prediction(models.Model):
    program = models.ForeignKey('Program', on_delete=models.CASCADE, default=1)  # Default to the ID 1 Program
    year = models.ForeignKey('CurriculumYear', on_delete=models.CASCADE, default=1)  # Default to the ID 1 CurriculumYear
    no_of_slot = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    input_data = models.JSONField()  # Assuming input data is stored as JSON
    predicted_result = models.FloatField()

    def __str__(self):
        return f"{self.program.program_name}"

