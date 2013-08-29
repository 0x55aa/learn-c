#coding: utf-8
from django.conf.urls import patterns, url
from stepbystep import views


urlpatterns = patterns('',
    url(r'course/(?P<pk>[0-9]+)/$', views.CourseView.as_view(), name='course'),
    url(r'list/$', views.CourseListView.as_view(), name='course_list'),
    url(r'judge_code/$', views.JudgeCodeView.as_view(), name='judge_code'),
)
