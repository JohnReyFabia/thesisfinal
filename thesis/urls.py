from django.urls import path
from . import views

urlpatterns=[
    path('', views.index_view, name = 'index'),
    path('college/', views.college_view, name='college'),
    path('college/program/<str:program>/', views.program_view, name='program'),
    path('about/', views.about_view, name='about'),

]