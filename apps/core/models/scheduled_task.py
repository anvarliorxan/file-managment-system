from django.db import models
from apps.user.models import File

class ScheduledTask(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='scheduled_task')
    task_name = models.CharField(max_length=255)
    scheduled_time = models.DateTimeField()
    task_id = models.CharField(max_length=255, blank=True, null=True)

    STATUS_CHOICES = (
        ("on_hold", 'On Hold'),
        ("completed", "Completed")
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=25, default='on_hold')

    def __str__(self):
        return f'{self.task_name} for {self.file.name} at {self.scheduled_time}'
