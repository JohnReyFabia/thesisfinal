from django.urls import path
from . import views

urlpatterns=[
    path('', views.index_view, name = 'index'),
    path('college/', views.college_view, name='college'),
    path('college/<str:code>/', views.program_view, name='program'),
    path('college/<str:code>/<str:program_name>/', views.get_selected_program, name='get_selected_program'),
    path('about/', views.about_view, name='about'),

]