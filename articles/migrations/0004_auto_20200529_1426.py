# Generated by Django 2.2.12 on 2020-05-29 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20200529_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, upload_to='articles_pictures/%Y/%m/%d/', verbose_name='文章图片'),
        ),
    ]
