from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.db import models
from django.core.mail import send_mail


SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class User(AbstractUser):
    gender = models.CharField(
        max_length=1,
        choices=(
            ('f', 'female'),
            ('m', 'male'),
        ),
        verbose_name='성별'
    )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website_url = models.URLField(blank=True)


def on_post_save_for_user(sender, **kwargs):
    # 가입 시기
    if kwargs['created']:
        user = kwargs['instance']

        # 환영 이메일 보내기
        send_mail(
            '환영합니다',
            '가입해주셔서 감사합니다',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )


post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    session_key = models.CharField(max_length=40, editable=False)
    created_at = models.DateField(auto_now_add=True)


def kick_my_other_session(sender, request, user, **kwargs):
    print('kicked my other login session')

    for user_session in UserSession.objects.filter(user=user):
        session_key = user_session.session_key
        session = SessionStore(session_key)
        # session.delete()
        session['kicked'] = True
        session.save()
        user_session.delete()

    session_key = request.session.session_key
    UserSession.objects.create(user=user, session_key=session_key)


user_logged_in.connect(kick_my_other_session)
