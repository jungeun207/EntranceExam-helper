from django.contrib import admin
from .models import University, Department, AdmissionInfo

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'region', 'established']
    list_filter = ['type', 'region']
    search_fields = ['name', 'description']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'college', 'capacity']
    list_filter = ['university', 'college']
    search_fields = ['name', 'description']

@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'university', 'admission_type', 'year']
    list_filter = ['admission_type', 'year', 'university']
    search_fields = ['title', 'description']