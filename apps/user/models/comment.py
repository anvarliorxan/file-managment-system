from django.db import models
from apps.user.models import User
from apps.user.models import File
from apps.core.models import TimeStampedModel

class Comment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return self.user.phone



