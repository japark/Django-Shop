# Generated by Django 3.0.7 on 2020-07-05 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_member_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(max_length=128, verbose_name='비밀번호'),
        ),
    ]
