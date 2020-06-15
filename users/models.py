#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from upload.models import UserImage


@python_2_unicode_compatible
class User(AbstractUser):
    """自定义用户模型"""
    nickname = models.CharField(null=True, blank=True, max_length=255, verbose_name='昵称')
    job_title = models.CharField(max_length=50, null=True, blank=True, verbose_name='职称')
    introduction = models.TextField(blank=True, null=True, verbose_name='简介')
    picture = models.ForeignKey(UserImage, null=True, related_name="im_user", on_delete=models.SET_NULL, verbose_name='头像')
    # picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name='')
    location = models.CharField(max_length=50, null=True, blank=True, verbose_name='城市')
    personal_url = models.URLField(max_length=555, blank=True, null=True, verbose_name='个人链接')
    facebook = models.URLField(max_length=255, blank=True, null=True, verbose_name='Facebook链接')
    google = models.URLField(max_length=255, blank=True, null=True, verbose_name='Google链接')
    github = models.URLField(max_length=255, blank=True, null=True, verbose_name='Github链接')
    linkedin = models.URLField(max_length=255, blank=True, null=True, verbose_name='Linkedin链接')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username
