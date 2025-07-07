from django.db import models

class University(models.Model):
    TYPE_CHOICES = [
        ('national', '국 · 공립대'),
        ('private', '사립대'),
    ]
    
    REGION_CHOICES = [
        ('seoul', '서울'),
        ('gyeonggi', '경기 · 인천'),
        ('gangwon', '강원'),
        ('chungbuk', '충북 · 충남 · 대전 · 세종'),
        ('jeonbuk', '전북 · 전남 · 광주'),
        ('gyeongbuk', '경북 · 경남 · 부산 · 대구 · 울산'),
        ('jeju', '제주'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="대학명")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="대학 유형")
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name="지역")
    address = models.CharField(max_length=200, verbose_name="주소")
    website = models.URLField(verbose_name="홈페이지")
    established = models.IntegerField(verbose_name="설립연도")
    description = models.TextField(verbose_name="대학 소개")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "대학"
        verbose_name_plural = "대학들"
    
    def __str__(self):
        return self.name

class Department(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="대학")
    name = models.CharField(max_length=100, verbose_name="학과명")
    college = models.CharField(max_length=100, verbose_name="단과대학")
    description = models.TextField(verbose_name="학과 소개")
    capacity = models.IntegerField(verbose_name="정원")
    
    class Meta:
        ordering = ['university', 'name']
        verbose_name = "학과"
        verbose_name_plural = "학과들"
    
    def __str__(self):
        return f"{self.university.name} - {self.name}"

class AdmissionInfo(models.Model):
    TYPE_CHOICES = [
        ('regular', '정시'),
        ('early', '수시'),
        ('special', '특별전형'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="대학")
    admission_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="전형 유형")
    title = models.CharField(max_length=200, verbose_name="전형명")
    description = models.TextField(verbose_name="전형 내용")
    requirements = models.TextField(verbose_name="지원 자격")
    selection_process = models.TextField(verbose_name="선발 방법")
    schedule = models.TextField(verbose_name="일정")
    year = models.IntegerField(verbose_name="학년도")
    
    class Meta:
        ordering = ['-year', 'university', 'admission_type']
        verbose_name = "입시 정보"
        verbose_name_plural = "입시 정보들"
    
    def __str__(self):
        return f"{self.university.name} - {self.title}"