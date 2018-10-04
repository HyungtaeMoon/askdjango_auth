from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required # 로그인되면 settings.LOGIN_URL 로 이동
def profile(request):
    request.user    # django.contrib.auth.models.AnonymousUser
    return render(request, 'accounts/profile.html')
