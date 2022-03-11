from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

##login page

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:  
            return render(request, 'login_boot.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login_boot.html')
    

###로그인 완료 후 이동 페이지
###management로 이동
def home(request):
    return render(request, 'management/index.html')