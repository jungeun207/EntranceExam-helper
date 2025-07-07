from django.shortcuts import render

def calculator_index(request):
    return render(request, 'calculator/index.html')

def grade_calculator(request):
    return render(request, 'calculator/grade.html')

def mock_exam_calculator(request):
    return render(request, 'calculator/mock_exam.html')