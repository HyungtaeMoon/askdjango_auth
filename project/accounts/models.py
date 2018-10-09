from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from django.core.mail import send_mail


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website_url = models.URLField(blank=True)


def on_post_save_for_user(sender, **kwargs):
    # 가입 시기
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)

        # 환영 이메일 보내기
        send_mail(
            '환영합니다',
            '가입해주셔서 감사합니다',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )


post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)
