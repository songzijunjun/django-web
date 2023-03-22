from django.db import models
from django.utils import timezone


class Account(models.Model):
    #an integer field representing the user's account type, with choices defined by the#
    #"Area_Level" tuple. The default value is set to 0, which corresponds to the "student" choice#
    Area_Level = (
        (0, 'student'),
        (1, 'teacher'),
        (2, 'manager'),
    )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40, null=False, verbose_name="username", unique=True)  # username
    password = models.CharField(max_length=256, null=False, verbose_name="password")  # password
    customer_type = models.IntegerField(default=0, choices=Area_Level, verbose_name="accountType")  # accountType
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)
