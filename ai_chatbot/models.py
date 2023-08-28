from django.db import models


class Log(models.Model):
    user_name = models.CharField('ユーザー名', max_length=30, null=True)
    title = models.CharField('質問のタイトル', max_length=100)
    text = models.TextField('内容', null=True)
    date = models.DateField('作成日時')
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class File(models.Model):
    user_name = models.CharField('ユーザー名', max_length=30, null=True)
    file_name = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='files/')
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.file_name
