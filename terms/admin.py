from django.contrib import admin
from .models import Term

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'definition']
    filter_horizontal = ['related_terms']