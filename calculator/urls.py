from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.calculator_index, name='index'),
    path('grade/', views.grade_calculator, name='grade'),
    path('mock-exam/', views.mock_exam_calculator, name='mock_exam'),
]