from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import SignupForm

'''
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })
'''

signup = CreateView.as_view(model=User,
                            form_class=SignupForm,
                            success_url=settings.LOGIN_URL,
                            template_name='accounts/signup.html'
                            )


@login_required # 로그인되면 settings.LOGIN_URL 로 이동
def profile(request):
    request.user    # django.contrib.auth.models.AnonymousUser
    return render(request, 'accounts/profile.html')
