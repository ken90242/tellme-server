# Generated by Django 2.2.12 on 2020-05-31 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_article_image2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
    ]