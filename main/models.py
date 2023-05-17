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

    description = models.TextField(default='', blank=True)


class ScheduleTableCell(models.Model):
    teacher = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    
    week_day_choices = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )

    week_day = models.IntegerField(choices=week_day_choices)

    row_number = models.IntegerField()

    html_class = 'active'
