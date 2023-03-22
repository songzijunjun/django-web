from django.utils import timezone

from django.db import models
from student.models import StudentInfo
from teacher.models import TeacherInfo


# Create your models here.


class Major(models.Model):
    id = models.BigAutoField(primary_key=True)
    major_code = models.CharField(max_length=32, verbose_name='majotCode', unique=True)
    name = models.CharField(max_length=32, verbose_name='majorName', unique=True)
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)


class Clazz(models.Model):
    #The information of class#
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='className')
    major_id = models.ForeignKey(Major, on_delete=models.CASCADE)
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)

    class Meta:
        unique_together = ('name', 'major_id',)


class ClazzStudents(models.Model):

    id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    clazz_id = models.ForeignKey(Clazz, on_delete=models.CASCADE)
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)

    class Meta:
        unique_together = ('student_id', 'clazz_id',)


class Curriculum(models.Model):
    #The class information#
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='className')
    teacher_id = models.ForeignKey(TeacherInfo, on_delete=models.CASCADE)  
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)

    class Meta:
        unique_together = ('name', 'teacher_id',)


class SchoolTimeTable(models.Model):
   #There are four class in a day#
    tt = (  
        (1, '8:00~9:40'),
        (2, '10:00~11:40'),
        (3, '14:00~15:40'),
        (4, '15:50~17:50'),
    )

    zz = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
    )

    id = models.BigAutoField(primary_key=True)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)  
    clazz_week = models.CharField(max_length=32, verbose_name='classWeek', choices=zz)  
    clazz_time = models.CharField(max_length=32, verbose_name='classTime', choices=tt)  
    clazz_id = models.ForeignKey(Clazz, on_delete=models.CASCADE) 
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)

    class Meta:
        unique_together = ('clazz_week', 'clazz_time', 'clazz_id')


class StudentCurriculumScore(models.Model):
    #The score of student#
    id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=1, max_digits=10)
    create_time = models.DateTimeField('createTime', default=timezone.now)
    update_time = models.DateTimeField('updateTime', default=timezone.now)

    class Meta:
        unique_together = ('student_id', 'curriculum_id')
