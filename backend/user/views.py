from user.models import User
from django.db.models.base import ModelState
from django.shortcuts import redirect, render
from django.contrib import auth


def signup(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        password_2 = request.POST.get('password_2')
        name = request.POST.get('name')
        student_id = request.POST.get('student_id')
        birth = request.POST.get('birth')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        github = request.POST.get('github')
        homepage = request.POST.get('homepage')

        # 입력 폼 점검
        message = ''
        if phone == '':
            message = "전화번호를 입력해 주세요."
        
        if email == '':
            message = "이메일을 입력해 주세요."
        
        if birth == '':
            message = "생일을 입력해 주세요."
        
        if student_id == '':
            message = "학번을 입력해 주세요."
        elif not len(student_id) == 10:
            message = "올바른 학번을 입력해 주세요."
        
        if name == '':
            message = "이름을 입력해 주세요."
        elif not len(name) <= 20:
            message = "이름이 너무 깁니다."
        
        if password == '':
            message = "비밀번호를 입력 해 주세요."
        elif not 6 <= len(password) <= 20:
            message = "올바른 비밀번호 길이를 입력 해 주세요."
        elif password != password_2:
            message = "비밀번호와 비밀번호 확인이 일치하지 않습니다."
        
        if user_id == '':
            message = "아이디를 입력 해 주세요."
        elif not 5 <= len(user_id) <= 20:
            message = "올바른 아이디 길이를 입력 해 주세요."
        
        if message != '':
            return render(request, 'signup.html', {'message': message})
        
        if github == '':
            github = 'null'
        if homepage == '':
            homepage = 'null'

        user = User.objects.create_user(
            user_id=user_id,
            password=password,
            name=name,
            student_id=student_id,
            birth=birth,
            email=email,
            phone=phone,
            github=github,
            homepage=homepage
        )
        auth.login(request, user)
        return redirect('index')
    else:
        if request.user.is_authenticated:
            auth.logout(request)
        return render(request, 'signup.html', {'message': "정보를 입력 해 주세요."})

def login(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        if user_id is '':
            return render(request, 'login.html', {'message': "아이디를 입력 해 주세요."})
        elif password is '':
            return render(request, 'login.html', {'message': "비밀번호를 입력 해 주세요."})

        user = auth.authenticate(request, user_id=user_id, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'message': "유저정보가 일치 하지 않습니다."})
    else:
        if request.user.is_authenticated:
            auth.logout(request)
        return render(request, 'login.html', {'message': "로그인 해 주세요."})


def logout(request):
    auth.logout(request)
    return redirect('index')