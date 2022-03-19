from audioop import reverse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse

##login page

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
            return redirect(reverse('analysis:dashboard_form'))
        
        else:
            if login_form.non_field_errors():
                return render(request, 'accounts/login_boot.html', {'error': login_form.non_field_errors()[0]}) 
    
            else:    
                 for field in login_form: 
                    for error in field.errors:
                       error_message = field.label + "을 입력해주세요\n"
                       return render(request, 'accounts/login_boot.html', {'error': field.label + " 입력해주세요"})     
                
    else:
         return render(request, 'accounts/login_boot.html')
     
# ###management로 이동
# def home(request):
#     return render(request, 'management/index.html')