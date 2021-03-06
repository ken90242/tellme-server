# Generated by Django 2.2.12 on 2020-06-07 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='verb',
            field=models.CharField(choices=[('L', 'Liked'), ('C', 'Commented on'), ('F', 'Added to favorites'), ('A', 'Answered'), ('W', 'Accepted the answer'), ('R', 'Replied to'), ('I', 'Logged in'), ('O', 'Logged out')], max_length=1, verbose_name='通知类别'),
        ),
    ]
