from django.db import models

class Term(models.Model):
    CATEGORY_CHOICES = [
        ('exam', '정시/수시 관련'),
        ('university', '대학 관련'),
        ('score', '성적 관련'),
        ('etc', '기타'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="용어명")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="카테고리")
    definition = models.TextField(verbose_name="정의")
    example = models.TextField(blank=True, null=True, verbose_name="예시")
    related_terms = models.ManyToManyField('self', blank=True, verbose_name="관련 용어")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "입시 용어"
        verbose_name_plural = "입시 용어들"
    
    def __str__(self):
        return self.name