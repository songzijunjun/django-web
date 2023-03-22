from django.db import models
from django.utils import timezone

from account.models import Account
# Create your models here.


class StudentInfo(models.Model):
    #The information of student#
    id = models.AutoField(primary_key=True)
    student_id = models.BigIntegerField(verbose_name="studentID")
    name = models.CharField(max_length=255, verbose_name="studentName")
    sex = models.CharField(max_length=10, verbose_name="Gender")
    birth_day = models.CharField(max_length=255, verbose_name="birthDate")
    native_place = models.CharField(max_length=255, verbose_name="hometown")
    major = models.CharField(max_length=255, verbose_name="major")
    clazz = models.CharField(max_length=255, verbose_name='class')
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="userID")
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)