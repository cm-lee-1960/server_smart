from audioop import reverse
from copyreg import constructor
from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
########################################################################################################################
# 로그인 뷰
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.18 - 로그인 에러 내용 출력
# 2022.03.24 - 에러내용 칼라변경
########################################################################################################################
def login(request):
    """메인페이지 로그인 화면 에러내용 추가"""
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
                            print(data)
                            return render(request, 'accounts/login_boot.html', data)     
                       else:
                            return render(request, 'accounts/login_boot.html', {'error': error_message , 'user_Name' : [0]}) 
    else:
         return render(request, 'accounts/login_boot.html', {'user_Name' : [0]})

#비밀번호 변경#
@login_required
def change_password(request):
  if request.method == "POST":
    user = request.user
    origin_password = request.POST["origin_password"]
    if check_password(origin_password, user.password):
      new_password = request.POST["new_password"]
      confirm_password = request.POST["confirm_password"]
      if new_password == confirm_password:
        if new_password != origin_password:
            user.set_password(new_password)
            user.save()
            auth.login(request, user)
            messages.success(request,'변경완료')
            return render(request, "accounts/change_password.html", {'error': '비밀번호가 변경되었습니다.'})
        else:
            messages.error(request, '이전 비밀번호와 일치합니다.')
            return render(request, "accounts/change_password.html", {'error': '이전 비밀번호와 일치합니다.'}) 
      else:
        messages.error(request, '비밀번호가 일치하지 않습니다.')
        return render(request, "accounts/change_password.html", {'error': '비밀번호가 일치하지 않습니다.'})
    else:
      messages.error(request, '비밀번호가 잘못 입력되었습니다.')
      return render(request, "accounts/change_password.html", {'error': '비밀번호가 잘못 입력되었습니다.'})
    messages.error(request, '비밀번호가 잘못 입력되었습니다.')
    return render(request, "accounts/change_password.html", {'error': '비밀번호가 잘못 입력되었습니다.'})
  else:
    messages.success(request,'오류')  
    return render(request, "accounts/change_password.html", {'error':'오류'})
#비밀번호 변경 화면#
@login_required
def change_password_page(request):
    """홈(Home) 페이지 뷰"""
    if request.user.is_authenticated:

        return render(request, "accounts/change_password.html")
    else:
        return redirect(reverse('accounts:login'))