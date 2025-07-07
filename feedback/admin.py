from django.contrib import admin
from .models import Feedback
from django.utils import timezone

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['subject', 'feedback_type', 'created_at', 'is_read', 'replied_at']
    list_filter = ['feedback_type', 'is_read', 'created_at']
    search_fields = ['subject', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('feedback_type', 'subject', 'created_at')
        }),
        ('내용', {
            'fields': ('message',)
        }),
        ('관리', {
            'fields': ('is_read', 'admin_reply', 'replied_at')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # 수정 중일 때
            return self.readonly_fields + ['feedback_type', 'subject', 'message']
        return self.readonly_fields
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()}개의 피드백을 읽음으로 표시했습니다.')
    mark_as_read.short_description = '읽음으로 표시'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'{queryset.count()}개의 피드백을 읽지 않음으로 표시했습니다.')
    mark_as_unread.short_description = '읽지 않음으로 표시'

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied_at:
            obj.replied_at = timezone.now()
        elif not obj.admin_reply:
            obj.replied_at = None
        super().save_model(request, obj, form, change)