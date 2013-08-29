# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

from stepbystep.models import Course


class TotalManager(models.Manager):
    def update_course(self, rel_user, course):
        total = Total.objects.get(user=rel_user)
        total.course = course
        total.save()
        return total


class Total(models.Model):
    user = models.OneToOneField(User, verbose_name="学生")
    #这里很二，default设置1,course 1不能删除
    course = models.ForeignKey(Course, verbose_name="做到哪一题", default=1)
    total_submit = models.IntegerField("总提交次数", default=0)
    success_submit = models.IntegerField("正确提交的次数", default=0)

    objects = TotalManager()

    def __unicode__(self):
        return self.user.username
