from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import University, Department, AdmissionInfo
import pandas as pd
from django.contrib import messages
import os
from django.conf import settings

def university_list(request):
    excel_file_path = os.path.join(settings.BASE_DIR, 'data', 'universities.csv')
    universities = []
    search = request.GET.get('search', '').strip()
    region = request.GET.get('region', '')
    type_uni = request.GET.get('type', '')
    
    try:
        df = pd.read_csv(excel_file_path)
        
        df.columns = df.columns.str.strip()
        
        name_col = '학교 이름'
        region_col = '지역'
        type_col = '국/공/사'
        link_col = '대학교 입학처 링크'
        
        df = df.dropna(subset=[name_col, link_col])
        
        # 지역 매핑
        region_mapping = {
            '서울': '서울',
            '경기': '경기 · 인천',
            '강원': '강원',
            '충청': '충북 · 충남 · 대전 · 세종',
            '전라': '전북 · 전남 · 광주',
            '경상': '경북 · 경남 · 부산 · 울산 · 대구',
            '제주': '제주'
        }
        
        # 유형 매핑
        type_mapping = {
            '국립': '국 · 공립',
            '특별법국립': '국 · 공립',
            '특별법법인': '국 · 공립',
            '공립': '국 · 공립',
            '사립': '사립'
        }
        
        # 데이터에 매핑된 카테고리 추가
        df['region_category'] = df[region_col].map(region_mapping)
        df['type_category'] = df[type_col].map(type_mapping)
        
        filtered_df = df.copy()
        
        if search:
            filtered_df = filtered_df[
                filtered_df[name_col].str.contains(search, case=False, na=False)
            ]
        
        if region:
            filtered_df = filtered_df[filtered_df['region_category'] == region]
        
        if type_uni:
            filtered_df = filtered_df[filtered_df['type_category'] == type_uni]
        
        # 지역 순서 정의
        region_order = {
            '서울': 1,
            '경기 · 인천': 2,
            '강원': 3,
            '충북 · 충남 · 대전 · 세종': 4,
            '전북 · 전남 · 광주': 5,
            '경북 · 경남 · 부산 · 울산 · 대구': 6,
            '제주': 7
        }
        
        # 지역 순서 컬럼 추가
        filtered_df['region_order'] = filtered_df['region_category'].map(region_order)
        
        # 지역 순서 -> 학교명 ㄱㄴㄷ순으로 정렬
        filtered_df = filtered_df.sort_values(['region_order', name_col])
        
        universities = []
        for _, row in filtered_df.iterrows():
            universities.append({
                'name': row[name_col],
                'region': row['region_category'],
                'type': row['type_category'],
                'recruitment_link': row[link_col]
            })
        
        # 지역 선택 옵션
        regions = [
            ('서울', '서울'),
            ('경기 · 인천', '경기 · 인천'),
            ('강원', '강원'),
            ('충북 · 충남 · 대전 · 세종', '충북 · 충남 · 대전 · 세종'),
            ('전북 · 전남 · 광주', '전북 · 전남 · 광주'),
            ('경북 · 경남 · 부산 · 울산 · 대구', '경북 · 경남 · 부산 · 울산 · 대구'),
            ('제주', '제주'),
        ]
        
        # 대학 유형 선택 옵션
        types = [
            ('국 · 공립', '국 · 공립'),
            ('사립', '사립'),
        ]
        
    except FileNotFoundError:
        messages.error(request, f'엑셀 파일을 찾을 수 없습니다: {excel_file_path}')
        universities = []
        regions = []
        types = []
    except Exception as e:
        messages.error(request, f'엑셀 파일을 읽는 중 오류가 발생했습니다: {str(e)}')
        universities = []
        regions = []
        types = []
    
    context = {
        'universities': universities,
        'search_query': search,
        'selected_region': region,
        'selected_type': type_uni,
        'regions': regions,
        'types': types,
    }
    
    return render(request, 'universities/list.html', context)