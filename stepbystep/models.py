# coding:utf-8
from django.db import models
from django.contrib.auth.models import User


class CourseManager(models.Manager):
    def create_detail(self, rel_user, form_data):
        course = self.create(
            user=rel_user,
            title=form_data['title'],
            content=form_data['content'],
            code=form_data['code'],
        )
        return course


class Course(models.Model):
    user = models.ForeignKey(User, verbose_name="创建用户")
    title = models.CharField("课程名", max_length=64)
    content = models.TextField("课程引导语", max_length=512)
    code = models.TextField("课程学习代码", max_length=1024)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    objects = CourseManager()

    def __unicode__(self):
        return self.title
