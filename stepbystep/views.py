# coding: utf-8
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from stepbystep.models import Course
from accounts.models import Total


class CourseView(DetailView):
    model = Course

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CourseView, self).dispatch(request, *args, **kwargs)

class CourseListView(ListView):
    model = Course
    paginate_by = '10'
    context_object_name = 'courses'


class JudgeCodeView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CourseView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        code = request.POST['code']
        course_id = request.POST['course_id']
        course = get_object_or_404(Course, id=course_id)
        if code == course.code:
            data['status'] = True
            course_data = Course.objects.filter(id__gt=course_id)
            if course_data.exists():
                next_course = course_data[0]
                total = Total.objects.update_course(user=request.user, course=next_course)
                data['course_id'] = total.course.id
            else:
                data['course_id'] = course_id
        else:
            data['status'] = False
        return HttpResponse(json.dumps(data), content_type="application/json")
