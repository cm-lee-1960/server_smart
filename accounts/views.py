from audioop import reverse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
import json

###################################################################################################
# 로그인 뷰
# -------------------------------------------------------------------------------------------------
# 2022-03-18 - 로그인 에러 내용 출력
# 2022-03-24 - 에러내용 칼라변경
###################################################################################################
##login page
##
def login(request):
    '''메인페이지 로그인 화면 에러내용 추가'''
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
    
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            #return redirect('http://localhost:8000/analysis/dashboard_form')
            return redirect(reverse('analysis:dashboard'))
        
        else:
            if login_form.non_field_errors():
                return render(request, 'accounts/login_boot.html', {'error': login_form.non_field_errors()[0]}) 
    
            else:    
                 for field in login_form: 
                    for error in field.errors:
                       error_message = field.label + "을 입력해주세요\n"
                       if field.label == "비밀번호":
                            print("잘들어왔따.")
                            print(username)
                            str_username = [str(username)]
                            print(str_username)
                            data = {
                                'error' : error_message,
                                'user_Name' : str_username
                            }
                            return render(request, 'accounts/login_boot.html', data)     
                       else:
                            return render(request, 'accounts/login_boot.html', {'error': error_message , 'user_Name' : [0]}) 
    else:
         return render(request, 'accounts/login_boot.html', {'user_Name' : [0]})
     
# ###management로 이동
# def home(request):
#     return render(request, 'management/index.html')