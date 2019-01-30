from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render, resolve_url, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView
from .forms import SignupForm, ProfileModel
from .models import Profile

'''
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # 로그인 처리
            next_url = request.GET.get('next') or 'profile'
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })
'''


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile'
        return resolve_url(next_url)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect(self.get_success_url())


signup = SignupView.as_view()

'''
signup = CreateView.as_view(model=User,
                            form_class=SignupForm,
                            success_url=settings.LOGIN_URL,
                            template_name='accounts/signup.html'
                            )
'''


# 로그인되면 settings.LOGIN_URL 로 이동
@login_required
def profile(request):
    # # 만약에 유저가 로그인을 한다면 프로필 페이지로 렌더를 해주고,
    # if request.user:    # django.contrib.auth.models.AnonymousUser
    #     return render(request, 'accounts/profile.html')
    # # 그게 아닐 경우에는 로그인 페이지로 보내줌
    # return redirect('accounts:login')

    # login_required 데코레이터를 사용하여,
    #   request.user 가 있을 경우에 accounts/profile.html 로 렌더해주고,
    #   그게 아닐 경우에는 settings.LOGIN_URL 설정 경로(login) 페이지로 보내줌
    if request.user:
        return render(request, 'accounts/profile.html')
    return redirect('accounts:profile')


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = ProfileModel
    success_url = reverse_lazy('profile')

    def get_object(self):
        # Profile 모델의 object 를 객체로 리턴시켜줌
        #   get_object 를 사용하면 urls.py 에 pk나 slug 를 전달하지 않고도
        #   업데이트 하고자 하는 유저의 프로필을 인식할 수 있음
        return self.request.user.profile


profile_edit = ProfileUpdateView.as_view()


class RequestLoginViaUrlView(PasswordResetView):
    # url 패턴은 login/url
    #   protocol + url + login_via_url(메서드)
    template_name = 'accounts/request_login_via_url_form.html'
    title = '이메일을 통한 로그인'
    # 유저에게 발송되는 이메일 양식으로 PasswordResetView 에서 정의되어있는 아래의 변수를
    #   오버라이딩 하여 사용함
    #   email_template_name = 'registration/password_reset_email.html'
    #       (이메일로 발송된) 아래의 주소를 통해 로그인하실 수 있습니다. 와 같은 템플릿
    email_template_name = 'accounts/login_via_url.html'
    success_url = settings.LOGIN_URL


def login_via_url(request, uidb64, token):
    # login 이 url 통해(via) 된다는 뜻에서 메서드명을 login_via_url 로 사용
    User = get_user_model()
    try:
        # 전자 메일을 통한 이진 전송 등에 많이 사용되는 base64(64진법)으로 매개변수 uidb64 를 디코딩
        uid = urlsafe_base64_decode(uidb64).decode()
        # 로그인을 하고자 하는 유저의 DB 에 접근하여 pk 값을 uid 로 할당
        #   uid 를 pk 로 할당함으로 인해서 url resolver 에서 따로 pk 를 받을 필요가 없음
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        raise Http404

    # current_user 는 로그인을 한 유저 object
    # uid 와 token 은 딕셔너리 타입으로 같이 받아야 함
    #   {'uidb64': 'Mw', 'token': '53e-74ab7afa29aba9xxxxxx'} 와 같은 키워드 인자 에러 발생
    #   또한 유저를 식별할 수 있는 토큰 값이 없으면 보안상의 문제가 발생할 것으로 예상
    if default_token_generator.check_token(current_user, token):
        # login 함수를 통한 로그인 처리
        auth_login(request, current_user)
        messages.info(request, '로그인이 승인되었습니다')
        # config.urls 에 root 로 정의시켜놓은 blog:post-list 로 리다이렉트
        return redirect('root')

    # 등록한 아이디가 없을 경우에 error 메시지를 출력
    #   현재 이 기능은 작동하지 않고, 템플릿에서도 보여지지 않는 상태로 수정이 필요
    messages.error(request, '로그인이 거부되었습니다')
    return redirect('root')


class MyPasswordChangeView(PasswordChangeView):
    """
    PasswordChangeView 안에는 아래의 클래스가 정의되어 있고, 사용자는 이를 이용하여 편하게 사용한다.
     1) request 받는 old_password 와 DB 에서 해당 유저의 password 를 비교
     2) cleaned_data 로 password1 과 password2 를 비교하여 저장
    """
    # PasswordChangeView 에 정의되어 있는 success_url, template_name 을 사용
    success_url = reverse_lazy('profile')
    #   아래의 admin 페이지를 새로 재정의 하여 사용
    # template_name = 'registration/password_change_form.html'
    template_name = 'accounts/password_change_form.html'

    def form_valid(self, form):
        # PasswordChangeView 의 form_valid 메서드를 재정의
        messages.info(self.request, '비밀번호 변경을 완료했습니다.')
        return super().form_valid(form)


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_form.html'
    # email_template_name = ...
    # html_email_template_name = ...

    def form_valid(self, form):
        messages.info(self.request, '비밀번호 변경 메일을 발송했습니다')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_confirm.html'

    def form_valid(self, form):
        messages.info(self.request, '비밀번호 초기화를 완료했습니다')
        return super().form_valid(form)
