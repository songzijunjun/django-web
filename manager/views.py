import traceback

from datetime import datetime

from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse

from utils.check_login import check_login
from utils.rendom_char import get_random_str

from .models import ClazzStudents, Major, Clazz, Curriculum, SchoolTimeTable
from teacher.models import TeacherInfo
from account.models import Account
from student.models import StudentInfo


@check_login
def manager_index(request):
    # Only students who have updated their class majors can view it
    all_students = ClazzStudents.objects.all()
    return render(request, 'admin_info.html', context={'students': all_students, 'title': 'All Student Information'})


@check_login
@transaction.atomic
def add_student_info(request):
    all_clazzs = Clazz.objects.all()
    if request.method == "GET":
        return render(request, 'add_student.html', context={'clazzs': all_clazzs, 'title': 'Add student'})
    if request.method == 'POST':
        params = request.POST.dict()
        for p in params.values():
            if not p:
                return render(request, 'add_student.html',
                              context={'messages': ['Incomplete data submitted'], 'clazzs': all_clazzs, 'title': 'Add student'})

        if Account.objects.filter(username=params['username']).exists():
            return render(request, 'add_student.html',
                          context={'messages': ['The account already exists, please change the account to submit'], 'clazzs': all_clazzs,
                                   'title': 'Add student'})

        account = Account(username=params['username'], password=make_password(
            params['password']), customer_type=0)
        account.save()
        _clazz = params['clazz_info'].split('-')
        _clazz_obj = Clazz.objects.get(id=_clazz[0])
        student = StudentInfo(name=params['name'], sex=params['sex'], birth_day=params['birth_day'],
                              native_place=params['native_place'], clazz=_clazz_obj.name,
                              major=_clazz_obj.major_id.name,
                              student_id=get_random_str(14, True), user_id=account)
        student.save()
        ClazzStudents(student_id=student, clazz_id=_clazz_obj).save()
        return render(request, 'add_student.html',
                      context={'messages': ['Successfully created a student account'], 'clazzs': all_clazzs, 'title': 'Add student'})


@check_login
def teachers_info(request):
    return render(request, 'admin_teacher.html',
                  context={'teachers': TeacherInfo.objects.all(), 'title': 'All teacher information'})


@check_login
@transaction.atomic
def add_teacher_info(request):
    if request.method == "GET":
        return render(request, 'add_teacher.html')
    if request.method == 'POST':
        params = request.POST.dict()
        for p in params.values():
            if not p:
                return render(request, 'add_teacher.html',
                              context={'messages': ['Incomplete data submitted'], 'title': 'Add teacher'})
        if Account.objects.filter(username=params['username']).exists():
            return render(request, 'add_teacher.html',
                          context={'messages': ['The account already exists, please change the registered account'], 'title': 'Add teacher'})
        account = Account(username=params['username'], password=make_password(
            params['password']), customer_type=1)
        account.save()
        TeacherInfo(name=params['name'], sex=params['sex'], birth_day=params['birth_day'],
                    teacher_id=get_random_str(14, True), user_id=account).save()
        return render(request, 'add_teacher.html', context={'messages': ['Successfully created a teacher account'], 'title': 'Add teacher'})


@check_login
def major(request):
    return render(request, 'major.html', context={'majors': Major.objects.all(), 'title': 'All majors'})


@check_login
def clazz(request):
    return render(request, 'clazz.html', context={'clazzs': Clazz.objects.all(), 'title': 'All classes'})


@check_login
def add_major(request):
    if request.method == 'GET':
        return render(request, 'add_major.html', context={'title': 'Add major'})
    else:
        params = request.POST.dict()
        for p in params.values():
            if not p:
                return render(request, 'add_major.html', context={'messages': ['Incomplete data submitted'], 'title': 'Add major'})
        try:
            Major(major_code=params['major_code'], name=params['name']).save()
            return render(request, 'add_major.html', context={'messages': ['Added new major successfully'], 'title': 'Add major'})
        except Exception as e:
            return render(request, 'add_major.html', context={'messages': ['Major already exists, creation failed'], 'title': 'Add major'})


@check_login
def add_clazz(request):
    all_majors = Major.objects.all()
    if request.method == 'GET':

        return render(request, 'add_clazz.html', context={'majors': all_majors, 'title': 'Add class'})
    else:
        params = request.POST.dict()
        for p in params.values():
            if not p:
                return render(request, 'add_clazz.html',
                              context={'messages': ['Incomplete data submitted'], 'majors': all_majors, 'title': 'Add class'})
        try:
            _major = params['major'].split('-')
            _major_obj = Major.objects.get(
                major_code=_major[0], name=_major[1])
            Clazz(name=params['name'], major_id=_major_obj).save()
            return render(request, 'add_clazz.html',
                          context={'messages': ['Added class successfully'], 'majors': all_majors, 'title': 'Add class'})
        except Exception as e:
            print(traceback.format_exc())
            return render(request, 'add_clazz.html',
                          context={'messages': ['Creation failed, please contact the administrator'], 'majors': all_majors, 'title': 'Add class'})


@check_login
def curriculum(request):
    return render(request, 'curriculum.html',
                  context={'curriculums': Curriculum.objects.all(), 'title': 'All curriculum information'})


@check_login
def add_curriculum(request):
    all_teachers = TeacherInfo.objects.all()
    if request.method == 'GET':
        return render(request, 'add_curriculum.html', context={'teachers': all_teachers, 'title': 'Add curriculum'})
    elif request.method == 'POST':
        params = request.POST.dict()
        for p in params.values():
            if not p:
                return render(request, 'add_curriculum.html',
                              context={'messages': ['Incomplete data submitted'], 'teachers': all_teachers, 'title': 'Add curriculum'})
        teacher = TeacherInfo.objects.get(
            id=params['teacher_info'].split('-')[0])
        Curriculum(name=params['name'], teacher_id=teacher).save()
        return render(request, 'add_curriculum.html',
                      context={'messages': ['Added curriculum successfully'], 'teachers': all_teachers, 'title': 'Add curriculum'})


@check_login
@transaction.atomic
def change_clazz_time_table(request):
    all_curr = Curriculum.objects.all()  # All classes
    context = {'curriculums': all_curr, 'title': 'Change class timetable'}

    if request.method == 'GET':
        clazz_id = request.GET.get('clazz_id')
    elif request.method == 'POST':
        clazz_id = request.POST.dict().get('clazz_id')
    else:
        return redirect('manager_index')

    def get_stt():
        tmp = {
            # The key is the first class, and the following dictionary is the day of the week
            '1': {'1': None, '2': None, '3': None, '4': None, '5': None},
            '2': {'1': None, '2': None, '3': None, '4': None, '5': None},
            '3': {'1': None, '2': None, '3': None, '4': None, '5': None},
            '4': {'1': None, '2': None, '3': None, '4': None, '5': None},
        }
        for stt in SchoolTimeTable.objects.filter(clazz_id=clazz_id).order_by('clazz_week'):
            tmp[str(stt.clazz_time)][str(stt.clazz_week)] = stt
        return tmp

    context['time_table'] = get_stt()
    context['clazz_id'] = clazz_id

    if request.method == 'GET':
        return render(request, 'change_clazz_time_table.html', context=context)
    elif request.method == 'POST':
        data = request.POST.dict()
        for k, v in data.items():
            if not v:
                context['messages'] = ['Submitted data is incomplete']
                return render(request, 'change_clazz_time_table.html',
                              context=context)
        week = data.get('week')
        table_time = data.get('table_time')
        _curriculum = data.get('curriculum')

        _curriculum = Curriculum.objects.get(id=_curriculum)
        if SchoolTimeTable.objects.filter(clazz_id=clazz_id, clazz_week=week, clazz_time=table_time).exists():
            SchoolTimeTable.objects.get(
                clazz_id=clazz_id, clazz_week=week, clazz_time=table_time).delete()

        print(clazz_id)
        SchoolTimeTable(clazz_id=Clazz.objects.get(id=clazz_id), clazz_time=table_time, clazz_week=week,
                        curriculum=_curriculum).save()
        context['messages'] = ['Added or changed successfully']
        context['time_table'] = get_stt()

        return render(request, 'change_clazz_time_table.html',
                      context=context)


@check_login
@transaction.atomic
def change_student_info(request):
    all_clazz = Clazz.objects.all()
    context = {'clazzs': all_clazz}

    if request.method == 'GET':
        student_id = request.GET.get('student_id')
    elif request.method == 'POST':
        student_id = request.POST.dict().get('student_id')
    else:
        return redirect('manager_index')

    print('student_id', student_id)
    current_clazz = ClazzStudents.objects.get(student_id=student_id)
    context['current_clazz_id'] = current_clazz.clazz_id
    context['sid'] = student_id
    context['student'] = StudentInfo.objects.get(id=student_id)

    if request.method == 'GET':
        return render(request, 'change_student_info.html', context=context)
    else:
        data = request.POST.dict()
        student_info = StudentInfo.objects.get(id=student_id)
        student_info.name = data['name']
        student_info.sex = data['sex']
        student_info.birth_day = data['birth_day']
        student_info.native_place = data['native_place']
        new_clazz = Clazz.objects.get(id=data['clazz'])
        student_info.major = new_clazz.major_id.name
        student_info.clazz = new_clazz.name
        student_info.update_time = datetime.now()
        student_info.save()
        cs = ClazzStudents.objects.get(student_id=student_id)
        cs.clazz_id = new_clazz
        cs.update_time = datetime.now()
        cs.save()
        context['current_clazz_id'] = new_clazz.id
        context['messages'] = ['Changed successfully']
        context['student'] = StudentInfo.objects.get(id=student_id)
        return render(request, 'change_student_info.html', context=context)


@check_login
@transaction.atomic
def change_teacher_info(request):
    if request.method == 'GET':
        teacher_id = request.GET.get('teacher_id')
    elif request.method == 'POST':
        teacher_id = request.POST.dict().get('teacher_id')
    else:
        return redirect('manager_index')

    teacher = TeacherInfo.objects.get(id=teacher_id)
    context = {'teacher': teacher}

    if request.method == "GET":
        return render(request, 'change_teacher_info.html', context)
    else:
        data = request.POST.dict()
        teacher.name = data['name']
        teacher.sex = data['sex']
        teacher.birth_day = data['birth_day']
        teacher.update_time = datetime.now()
        teacher.save()
        context = {'teacher': teacher, 'messages': ['Changed successfully']}
        return render(request, 'change_teacher_info.html', context)


@check_login
@transaction.atomic
def delete_student(request):
    sid = request.GET.get('id')
    if not sid:
        return 'Request parameter error'
    if not StudentInfo.objects.filter(id=sid).exists():
        return 'Parameter error'
    student = StudentInfo.objects.get(id=sid)
    student.delete()
    if Account.objects.filter(id=student.user_id.id).exists():
        Account.objects.filter(id=student.user_id.id).delete()
    return JsonResponse({'success': True, 'message': 'Deleted successfully'})


@check_login
@transaction.atomic
def delete_teacher(request):
    tid = request.GET.get('id')
    if not tid:
        return 'Request parameter error'
    if not TeacherInfo.objects.filter(id=tid).exists():
        return 'Parameter error'
    teacher = TeacherInfo.objects.get(id=tid)
    teacher.delete()
    if Account.objects.filter(id=teacher.user_id.id).exists():
        Account.objects.filter(id=teacher.user_id.id).delete()
    return JsonResponse({'success': True, 'message': 'Deleted successfully'})
