# coding: utf-8
from django.db import models
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.auth.models import User


class Comment(BaseCommentAbstractModel):
    comment = models.TextField('评论', max_length=300)
    user = models.ForeignKey(User)
