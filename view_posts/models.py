from django.db import models

# Create your models here.

class Posts(models.Model):
    title = models.CharField(max_length=128)  # 名字长
    created = models.DateField(auto_now_add=True)  # 文章创建日期
    content = models.TextField()








