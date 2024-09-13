from django.db import models
from apps.core.models import TimeStampedModel
import os
from django.core.validators import FileExtensionValidator
from apps.user.models import User


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class File(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    TYPE_CHOICES = (
        ("public", 'Public'),
        ("private", 'Private'),
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='user_files',
                            validators=[FileExtensionValidator(allowed_extensions=['png', 'doc', 'pptx'])])
    type = models.CharField(max_length=25, choices=TYPE_CHOICES, default="public")
    share_link = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField(blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='files')

    expiration_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file:
            original_name = os.path.basename(self.file.name)
            self.name = original_name.lower().replace(' ', '_')
        super().save(*args, **kwargs)



