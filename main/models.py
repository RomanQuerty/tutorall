from django.db import models
from django.conf import settings


# Create your models here.


class AppUser(models.Model):
    django_user_ref = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='app_user',
    )

    STUDENT = 0
    TEACHER = 1

    user_type_choices = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
    )

    user_type = models.IntegerField(
        default=STUDENT,
        choices=user_type_choices
    )

    description = models.TextField(default='')
