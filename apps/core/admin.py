from django.contrib import admin
from apps.core.models.scheduled_task import ScheduledTask  # Update with your actual import path

@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ('file', 'task_name', 'scheduled_time', 'task_id')
    list_filter = ('scheduled_time',)
    search_fields = ('file__name', 'task_name')