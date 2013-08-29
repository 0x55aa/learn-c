# coding: utf-8
import os
import json
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class ExerciseManager(models.Manager):
    def create_detail(self, rel_user, form_data):
        exercise = self.create(
            user=rel_user,
            title=form_data['title'],
            content=form_data['content'],
            input_text=form_data['input_text'],
            output_text=form_data['output_text'],
        )
        return exercise


class Exercise(models.Model):
    SORT_CHOICES = (
        #练习
        (1, '顺序结构'),
        (2, '选择结构'),
        (3, '循环结构'),
        (4, '数组'),
        (5, '指针'),
        (6, '结构体'),
        #作业
        (7, '作业'),
        #考试
        (8, '考试'),
    )

    user = models.ForeignKey(User, verbose_name="创建的用户")
    title = models.CharField("练习题名", max_length=64)
    content = models.TextField("练习题目", max_length=512)
    input_text = models.TextField("输入", max_length=512, blank=True)
    output_text = models.TextField("程序预定输出", max_length=512)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    total_submit = models.IntegerField("总提交次数", default=0)
    success_submit = models.IntegerField("正确提交的次数", default=0)
    sort = models.IntegerField("题目分类", choices=SORT_CHOICES, default=1)


    objects = ExerciseManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Exercise, self).save(*args, **kwargs)
        code_path = os.path.join(settings.ROOT, 'code')
        input_path = os.path.join(code_path, 'input')
        #output_path = os.path.join(code_path, 'output')
        input_file = input_path + '/' + str(self.id) + '.input'
        #output_file = output_path + '/' + str(self.id) + '.output'
        f = open(input_file, 'w')
        f.write(self.input_text)
        f.close()
        #f = open(output_file, 'w')
        #f.write(self.output_text)
        #f.close()


class SubmitManager(models.Manager):
    def create_submit(self, rel_user, form_data):
        exercise = self.create(
            user=rel_user,
            exercise=form_data['exercise'],
            code=form_data['code'],
            cpu_time=form_data['cpu_time'],
            mem=form_data['mem'],
            status=form_data['status'],
        )
        return exercise


class Submit(models.Model):
    STATUS_CHOICES = (
        (1, '编译失败'),
        (2, '逻辑错误'),
        (3, '成功'),
        (4, '运行错误'),
        (5, '未知错误'),
        (6, '正在编译'),
    )
    user = models.ForeignKey(User, verbose_name="提交答案的学生")
    exercise = models.ForeignKey(Exercise, verbose_name="提交的哪一个题")
    code = models.CharField("提交的代码", max_length=1024)
    cpu_time = models.IntegerField("cpu执行时间,ms", default=0)
    mem = models.IntegerField("消耗内存,kb", default=0)
    status = models.IntegerField("代码状态", choices=STATUS_CHOICES, default=6)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    objects = SubmitManager()

    def __unicode__(self):
        return '%s-%s' % (self.user.username, self.exercise.title)
