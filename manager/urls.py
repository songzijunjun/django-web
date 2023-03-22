"""student_manager_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import *

urlpatterns = [
    path('manager_index/', manager_index, name='manager_index'),
    path('majors/', major, name='majors'),
    path('clazzs/', clazz, name='clazzs'),
    path('add_clazz/', add_clazz, name='add_clazz'),
    path('add_major/', add_major, name='add_major'),
    path('curriculum/', curriculum, name='curriculum'),
    path('add_curriculum/', add_curriculum, name='add_curriculum'),
    path('teachers_info/', teachers_info, name='teachers_info'),
    path('add_teacher_info/', add_teacher_info, name='add_teacher_info'),
    path('add_student_info/', add_student_info, name='add_student_info'),
    path('change_clazz_time_table/', change_clazz_time_table, name='change_clazz_time_table'),
    path('change_student_info/', change_student_info, name='change_student_info'),
    path('change_teacher_info/', change_teacher_info, name='change_teacher_info'),
    path('delete_student/', delete_student, name='delete_student'),
    path('delete_teacher/', delete_teacher, name='delete_teacher'),

]
