from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import File
from apps.core.utils import generate_file_share_link
import pytz
from datetime import datetime, timedelta
from apps.taskapp.tasks import remove_file
from apps.core.models.scheduled_task import ScheduledTask
from django.conf import settings


@receiver(post_save, sender=File)
def create_private_file_share_link(sender, instance, created, **kwargs):
    if created and instance.type == 'private':
        instance.share_link = generate_file_share_link(instance)
        instance.save()



@receiver(post_save, sender=File)
def set_file_expiration_date(sender, instance, created, **kwargs):
    if created:
        local_tz = pytz.timezone(settings.TIME_ZONE)
        now = datetime.now(local_tz)
        run_at = now.replace(month=instance.expiration_date.month, day=instance.expiration_date.day)
        task_run_time = run_at.astimezone(pytz.utc)

        scheduled_task = ScheduledTask.objects.create(
            file=instance,
            task_name='Remove file',
            scheduled_time=task_run_time,
        )

        task_id = remove_file.apply_async(eta=task_run_time, args=[instance.id, ]).id

        scheduled_task.task_id = task_id
        scheduled_task.save()