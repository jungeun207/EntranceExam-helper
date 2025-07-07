from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('feedback', '피드백'),
        ('term_request', '용어 요청'),
        ('question', '질문'),
        ('bug_report', '버그 신고'),
        ('etc', '기타'),
    ]

    feedback_type = models.CharField(
        max_length=20, 
        choices=FEEDBACK_TYPE_CHOICES,
        default='feedback',
        verbose_name='유형'
    )
    subject = models.CharField(max_length=200, verbose_name='제목')
    message = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='작성일')
    is_read = models.BooleanField(default=False, verbose_name='읽음')
    admin_reply = models.TextField(blank=True, verbose_name='관리자 답변')
    replied_at = models.DateTimeField(null=True, blank=True, verbose_name='답변일')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '피드백'
        verbose_name_plural = '피드백'
    
    def __str__(self):  
        return self.subject