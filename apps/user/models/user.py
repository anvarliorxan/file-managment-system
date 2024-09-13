from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from apps.core.models import TimeStampedModel
from apps.core.utils import phone_regex, phone_message
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings
from django.utils.crypto import get_random_string


class UserAccountManager(BaseUserManager):

    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must provide a username to create an account')

        user = self.model(
            username=username
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None):

        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser, TimeStampedModel):
    USER_TYPE_CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin'),
    )

    user_type = models.CharField(max_length=25, choices=USER_TYPE_CHOICES, default="user")

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
        blank=True
    )

    phone = models.CharField(validators=[phone_regex],
                                help_text=phone_message,
                                max_length=12,
                                unique=True,
                                null=True,
                                blank=True)

    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)


    def get_user_type(self):
        return self.user_type


    def set_password(self, raw_password):
        if raw_password:
            super().set_password(raw_password)
        else:
            self.password = None

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)


