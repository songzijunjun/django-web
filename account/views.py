from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .models import Account


def index(request):
    is_login = request.session.get('is_login', False)
    if not is_login:
        return redirect('login')
    user_id = request.session.get('user_id')
    account = Account.objects.get(id=user_id)
    if account.customer_type == 0:
        return redirect('student_info')
    elif account.customer_type == 1:
        return redirect('teacher_info')
    return redirect('manager_index')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username or not password:
            return render(request, 'login.html', context={'messages': ['Submitted information is incomplete']})
        if not Account.objects.filter(username=username).exists():
            return render(request, 'login.html', context={'messages': ['User does not exist']})

        account = Account.objects.filter(username=username)[0]
        if not check_password(password, account.password):
            return render(request, 'login.html', context={'messages': ['Incorrect password']})

        request.session['is_login'] = 'true'
        request.session['username'] = account.username
        request.session['user_id'] = account.id
        request.session['customer_type'] = account.customer_type
        if account.customer_type == 0:
            return redirect('student_info')
        elif account.customer_type == 1:
            return redirect('teacher_info')
        return redirect('manager_index')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password_again = request.POST.get('password-again', None)
        typ = request.POST.get('cus_typ', None)
        if not username or not password or not password_again or not typ:
            return render(request, 'register.html', context={'messages': ['Submitted information is incomplete']})
        if password_again != password:
            return render(request, 'register.html', context={'messages': ['The two entered passwords do not match']})
        if Account.objects.filter(username=username).exists():
            return render(request, 'register.html', context={'messages': ['User already exists']})
        Account(username=username, password=make_password(
            password), customer_type=typ).save()
        return redirect('/login')


def logout(request):
    # 1. Delete the username and nickname in the session
    request.session.flush()
    # 2. Redirect to login screen
    return redirect('login')
