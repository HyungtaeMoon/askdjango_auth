from django.contrib.auth import views as auth_views

from . import views
from django.urls import path, reverse_lazy

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # CBV 로 로그인 기능을 구현, 기본 template_name 은 'registration/login.html' 을 커스텀하기 위해 아래와 같이 변경
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # CBV 로 로그아웃 기능을 구현, settings 또는 템플릿 파일에서 다음 페이지의 리다이렉트 경로를 설정하는 것을 추천
    #   그렇지 않다면 admin 페이지의 로그아웃 템플릿이 사용되어짐
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    # get_object 메서드를 오버라이딩하여 유저를 식별할 수 있어, <int:pk> 값이 없어도 됨
    path('profile/edit', views.profile_edit, name='profile_edit'),

    # 이메일로 로그인하기 에 접근하여 PasswordResetView 를 사용한 이메일로 로그인하기 기능 구현
    #   email_template_name 이 원래 reset form 이었으나 login_via_url.html 로 양식을 변경
    path('login/url', views.RequestLoginViaUrlView.as_view(), name='request_login_via_url'),
    # uid=base64(64진법) 으로 인코딩 된 데이터를 디코딩, str 타입의 토큰을 받아 처리
    path('login/<uidb64>/<token>/', views.login_via_url, name='login_via_url'),

    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
    #     template_name='accounts/password_change_done.html'
    # ), name='password_change_done'),

    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
