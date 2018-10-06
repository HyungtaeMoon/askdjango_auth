# Generated by Django 2.1.2 on 2018-10-06 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def forward_func(apps, schema_editor):
    # 현재 모든 User에 대해서 Profile을 만들어줍니다.
    auth_user_model = settings.AUTH_USER_MODEL.split('.')   #'auth.User
    User = apps.get_model(*auth_user_model)
    Profile = apps.get_model('accounts', 'Profile')

    for user in User.objects.all():
        print('create profile for user#{}'.format(user.pk))
        Profile.objects.create(user=user)


def backward_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('website_url', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(forward_func, backward_func),
    ]