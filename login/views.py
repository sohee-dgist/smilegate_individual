from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import redis
import datetime
from .api import myapis
# Create your views here.

def login(request):
    if request.method == 'POST':
        r = redis.Redis("localhost")
        userid = request.POST["id"]
        userpassword = request.POST["real"]
        if User.objects.filter(id=userid).exists():
            u = User.objects.get(id=userid)
            if u.password == userpassword:
                token = myapis.tokens.make_token(userid)
                refresh_token = myapis.tokens.make_refresh_token(userid)
                response = redirect('main:main')
                response.set_cookie('token', token.decode('utf-8'))
                response.set_cookie('refresh_token', refresh_token.decode('utf-8'))
                cache_key = userid
                cache_value = refresh_token
                r.set(cache_key, cache_value)
                u.refresh_token = refresh_token
                u.save()
                return response
            else:
                messages.warning(request, '비밀번호가 다릅니다.')
        else:
            messages.warning(request, '해당 id가 존재하지 않습니다.')
    return render(request, 'login/loginpage.html')

def signin(request):
    if request.method == 'POST':
        if User.objects.filter(id=request.POST['id']).exists():
            messages.warning(request, '중복된 아이디입니다.')
            return redirect('main:signin')
        u = User(id=request.POST['id'], password=request.POST['real'], sign_date= datetime.datetime.now())
        u.save()
        return redirect('main:login')
    return render(request, 'login/signpage.html')

def main(request):
    r = redis.Redis("localhost")
    current_token = request.COOKIES.get('token')
    flag, user_id = myapis.tokens.check_token(current_token)
    if flag == True:
        #token valid
        return render(request, 'login/main.html', {'userid':user_id})
    else:
        #token expired
        response = render(request, 'login/main.html', {'userid':user_id})
        refresh_token = request.COOKIES.get('refresh_token')
        flag, user_id = myapis.tokens.check_refresh_token(refresh_token)
        if flag == True:
            if r.exists(user_id) != 1:
                return redirect('main:login')
            if refresh_token == r.get(user_id).decode('utf-8'):
                new_token = myapis.tokens.make_token(user_id)
                response.set_cookie('token', new_token.decode('utf-8'))
                return response
            else:
                u = User.objects.get(id=user_id)
                if refresh_token == u.refresh_token:
                    new_token = myapis.tokens.make_token(user_id)
                    response.set_cookie('token', new_token.decode('utf-8'))
                    return response
                else:
                    messages.warning(request, '토큰이 유효하지 않습니다.')
                    return response
        else:
            messages.warning(request, '로그인 유효 시간이 만료되었습니다.')
            return response
def logout(request):
    response = render(request, 'login/loginpage.html')
    response.delete_cookie('token')
    response.delete_cookie('refresh_token')
    return response

def findpw(request):
    pass

def email(request):
    pass

def signout(request):
    current_token = request.COOKIES.get('token')
    flag, user_id = myapis.tokens.check_token(current_token)
    if flag:
        u = User.objects.get(id=user_id)
        u.delete()
        u.save()
        return redirect('main:login')
    else:
        return redirect('main:main')