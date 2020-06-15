from django.db import models

class ArticleImage(models.Model):
    file = models.ImageField(upload_to='articles_pictures/%Y/%m/%d/', blank=False, null=False)
    def __str__(self):
        return self.file.name

class UserImage(models.Model):
    file = models.ImageField(upload_to='profile_pics/', blank=False, null=False)
    def __str__(self):
        return self.file.name

