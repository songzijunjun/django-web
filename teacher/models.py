from django.db import models
from django.utils import timezone

from account.models import Account


class TeacherInfo(models.Model):
    #The teacher information#
    id = models.AutoField(primary_key=True)
    teacher_id = models.BigIntegerField(verbose_name="teacherID")
    name = models.CharField(max_length=255, verbose_name="teacherName")
    sex = models.CharField(max_length=10, verbose_name="Gender")
    birth_day = models.CharField(max_length=255, verbose_name="birthDate")
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="userID")
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)