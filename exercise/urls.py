#coding: utf-8
from django.conf.urls import patterns, url
from exercise import views


urlpatterns = patterns('',
    url(r'(?P<pk>[0-9]+)/$', views.ExerciseView.as_view(), name='exercise_subject'),
    url(r'list/$', views.ExerciseListView.as_view(), name='exercise_list'),
    url(r'submit/$', views.SubmitView.as_view(), name='submit'),
)
