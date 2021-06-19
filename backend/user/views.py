from user.models import User
from django.db.models.base import ModelState
from django.shortcuts import redirect, render
from django.contrib import auth, messages


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
        if phone == '':
            messages.error(request, "전화번호를 입력 해 주세요.")
        elif email == '':
            messages.error(request, "이메일을 입력해 주세요.")
        elif birth == '':
            messages.error(request, "생일을 입력해 주세요.")
        elif student_id == '':
            messages.error(request, "학번을 입력해 주세요.")
        elif not len(student_id) == 10:
            messages.error(request, "올바른 학번을 입력해 주세요.")
        elif name == '':
            messages.error(request, "이름을 입력해 주세요.")
        elif not len(name) <= 20:
            messages.error(request, "이름이 너무 깁니다.")
        elif password == '':
            messages.error(request, "비밀번호를 입력 해 주세요.")
        elif not 6 <= len(password) <= 20:
            messages.error(request, "올바른 비밀번호 길이를 입력 해 주세요.")
        elif password != password_2:
            messages.error(request, "비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        elif user_id == '':
            messages.error(request, "아이디를 입력 해 주세요.")
        elif not 5 <= len(user_id) <= 20:
            messages.error(request, "올바른 아이디 길이를 입력 해 주세요.")
        
        if len(messages.get_messages(request)) != 0:
            return render(request, 'signup.html', {'message': '정보를 입력 해 주세요.'})
        
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
        messages.success(request, "성공적으로 회원 가입이 완료 되었습니다.")
        return redirect('index')
    else:
        if request.user.is_authenticated:
            auth.logout(request)
        return render(request, 'signup.html', {'message': "정보를 입력 해 주세요."})

def login(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        if user_id == '':
            return render(request, 'login.html', {'message': "아이디를 입력 해 주세요."})
        elif password == '':
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