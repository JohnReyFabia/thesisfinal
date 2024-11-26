from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('college/', views.college_view, name='college'),
    path('college/<str:code>/', views.program_view, name='program'),
    path('college/<str:code>/<str:program_name>/', views.get_selected_program, name='get_selected_program'),
    path('about/', views.about_view, name='about'),
    path('upload/', views.upload_file, name='upload_file'),  
    path('college/<str:code>/', views.program_view, name='program'),
    path('college/<str:code>/<str:program_name>/', views.get_program_details, name='get_program_details'),
    path('check_slots/', views.check_no_of_slot, name='check_no_of_slot'),
    path('fetch_program_data/', views.fetch_program_data, name='fetch_program_data'),

]
