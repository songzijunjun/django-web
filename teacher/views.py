from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from utils.check_login import check_login

from account.models import Account
from .models import TeacherInfo
from student.models import StudentInfo
from manager.models import Curriculum, SchoolTimeTable, ClazzStudents, StudentCurriculumScore

from utils.rendom_char import get_random_str


@check_login
def teacher_info(request):
    user_id = request.session.get('user_id')
    req_typ = request.GET.get('typ')

    if request.method == 'GET':
        if not req_typ:
            if not TeacherInfo.objects.filter(user_id=user_id).exists():
                return render(request, 'teacher_info.html',
                              context={'teacher_id': 'Not set', 'name': 'Not set', 'sex': 'Not set',
                                       'birth_day': 'Not set'})
            info = TeacherInfo.objects.get(user_id=user_id)
            return render(request, 'teacher_info.html', context=info.__dict__)
        elif req_typ.upper() == 'update'.upper():
            context = {'typ': 'update', }
            if TeacherInfo.objects.filter(user_id=user_id).exists():
                context['tid'] = TeacherInfo.objects.get(user_id=user_id).id
            return render(request, 'teacher_info.html', context=context)
        elif req_typ.upper() == 'change_password'.upper():
            return render(request, 'teacher_info.html', context={'typ': 'change_password'})
    elif request.method == 'POST':
        params = request.POST.dict()
        if params.get('req_typ') == 'info':
            if not params.get('name') or not params.get('sex') or not params.get('birth_day'):
                return render(request, 'teacher_info.html', context={'typ': 'update', 'message': 'Submitted data is incomplete'})

            TeacherInfo(name=params['name'], sex=params['sex'], birth_day=params['birth_day'],
                        teacher_id=params.get(
                            'teacher_id', get_random_str(14, True)),
                        user_id=Account.objects.get(id=user_id)).save()

            return redirect('/teacher_info/')
        elif params.get('req_typ') == 'password':
            password = params.get('password')
            password_again = params.get('password-again')
            if password_again != password:
                return render(request, 'teacher_info.html',
                              context={'typ': 'change_password', 'message': 'The two entered passwords do not match'})
            account = Account.objects.get(id=user_id)
            account.password = make_password(password)
            account.save()
            return render(request, 'teacher_info.html', context={'typ': 'change_password', 'message': 'Change password complete'})


@check_login
def teacher_time_table(request):
    user_id = request.session.get('user_id')

    if not TeacherInfo.objects.filter(user_id=user_id).exists():
        return redirect('teacher_info')

    teacher = TeacherInfo.objects.get(user_id=user_id)

    def get_stt():
        tmp = {
            # The key is the first class, and the following dictionary is the day of the week
            '1': {'1': [], '2': [], '3': [], '4': [], '5': []},
            '2': {'1': [], '2': [], '3': [], '4': [], '5': []},
            '3': {'1': [], '2': [], '3': [], '4': [], '5': []},
            '4': {'1': [], '2': [], '3': [], '4': [], '5': []},
        }
        for stt in SchoolTimeTable.objects.filter(curriculum__teacher_id=teacher.id).order_by('clazz_week'):
            tmp[str(stt.clazz_time)][str(stt.clazz_week)].append(stt)
        return tmp

    return render(request, 'teacher_info.html', context={'time_table': get_stt(), 'typ': 'curriculum'})


@check_login
def teacher_input_score(request):
    if request.method == 'POST':
        data = request.POST.dict()
        if not StudentCurriculumScore.objects.filter(student_id__student_id=data['student_id'],
                                                     curriculum_id=data['curriculum_id']).exists():
            scs = StudentCurriculumScore(student_id=StudentInfo.objects.get(student_id=data['student_id']),
                                         curriculum_id=Curriculum.objects.get(id=data['curriculum_id']))
        else:
            scs = StudentCurriculumScore.objects.get(
                student_id__student_id=data['student_id'], curriculum_id=data['curriculum_id'])
        scs.score = data['score']
        scs.save()

    user_id = request.session.get('user_id')

    if not TeacherInfo.objects.filter(user_id=user_id).exists():
        return redirect('teacher_info')

    teacher = TeacherInfo.objects.get(user_id=user_id)

    clazz_and_curriculum_ids = []
    for stt in SchoolTimeTable.objects.filter(curriculum__teacher_id=teacher.id):
        _clazz_id = stt.clazz_id.id
        _curr_id = stt.curriculum.id
        if (_clazz_id, _curr_id) not in clazz_and_curriculum_ids:
            clazz_and_curriculum_ids.append((_clazz_id, _curr_id))

    all_students = []
    all_scores = []
    all_curriculums = []
    for ci in clazz_and_curriculum_ids:
        cs = ClazzStudents.objects.filter(clazz_id=ci[0])
        all_students += cs
        for _c in cs:
            _score = StudentCurriculumScore.objects.filter(
                student_id=_c.student_id.id, curriculum_id=ci[1])
            if _score:
                all_scores.append(str(_score[0].score))
            else:
                all_scores.append('-')
            all_curriculums.append(Curriculum.objects.get(id=ci[1]))
    return render(request, 'teacher_info.html',
                  context={'students': zip(all_students, all_scores, all_curriculums),
                           'typ': 'score'})
