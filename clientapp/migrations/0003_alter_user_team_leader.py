# Generated by Django 4.0.6 on 2022-07-15 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0002_alter_office_options_alter_teamleader_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_lead', to='clientapp.teamleader'),
        ),
    ]
