from django.shortcuts import render
from django.db.models import Q
from .models import Term
import pandas as pd
from django.contrib import messages
import os
from django.conf import settings

def terms_list(request):
    excel_file_path = os.path.join(settings.BASE_DIR, 'data', 'terms.csv')
    
    terms = []
    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', '')

    search_performed = bool(search_query or selected_category)
    
    try:
        df = pd.read_csv(excel_file_path)
        
        df.columns = df.columns.str.strip()
        
        name_col = '용어 이름'
        category_col = '카테고리'
        definition_col = '뜻'
        
        df = df.dropna(subset=[name_col, definition_col])
        filtered_df = df.copy()

        if search_query:
            filtered_df = filtered_df[
                filtered_df[name_col].str.contains(search_query, case=False, na=False)
            ]
        
        if selected_category:
            filtered_df = filtered_df[filtered_df[category_col] == selected_category]
        
        terms = []
        for _, row in filtered_df.iterrows():
            terms.append({
                'name': row[name_col],
                'category': row[category_col],
                'definition': row[definition_col]
            }) 
        
        unique_categories = df[category_col].dropna().unique()
        categories = [(cat, cat) for cat in unique_categories]

    except FileNotFoundError:
        messages.error(request, f'엑셀 파일을 찾을 수 없습니다: {excel_file_path}')
        terms = []
        categories = []
    except Exception as e:
        messages.error(request, f'엑셀 파일을 읽는 중 오류가 발생했습니다: {str(e)}')
        terms = []
        categories = []
    
    context = {
        'terms': terms,
        'search_query': search_query,
        'selected_category': selected_category,
        'search_performed': search_performed,
        'categories' : categories,
    }
    
    return render(request, 'terms/list.html', context)