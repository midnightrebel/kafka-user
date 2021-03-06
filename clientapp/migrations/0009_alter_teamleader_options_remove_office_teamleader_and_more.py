# Generated by Django 4.0.6 on 2022-07-19 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0008_user_teamleader'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamleader',
            options={'ordering': ['language'], 'verbose_name': 'Тим-лидер', 'verbose_name_plural': 'Тим-лидеры'},
        ),
        migrations.RemoveField(
            model_name='office',
            name='teamleader',
        ),
        migrations.RemoveField(
            model_name='teamleader',
            name='email',
        ),
        migrations.RemoveField(
            model_name='teamleader',
            name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='teamleader',
        ),
        migrations.AddField(
            model_name='teamleader',
            name='language',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='teamleader',
            name='office',
            field=models.ManyToManyField(to='clientapp.office'),
        ),
        migrations.AddField(
            model_name='teamleader',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
