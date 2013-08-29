# coding: utf-8
import os
import json
import commands
from django.http import HttpResponse
from django.views.generic import DetailView, View
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.conf import settings
from exercise.models import Exercise, Submit
from exercise import run


class ExerciseView(DetailView):
    model = Exercise

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ExerciseView, self).dispatch(request, *args, **kwargs)

class ExerciseListView(ListView):
    model = Exercise
    paginate_by = '10'
    context_object_name = 'exercises'


class SubmitView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SubmitView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        user = request.user
        data = {}
        code = request.POST['code']
        exercise_id = request.POST['exercise_id']
        exercise = get_object_or_404(Exercise, id=exercise_id)
        exercise.total_submit += 1
        user.total.total_submit += 1
        submit = Submit(
            user=user,
            exercise=exercise,
            code=code,
            code_len=len(code),
        )
        submit.save()
        #编译执行需要独立执行，容易超时:
        code_path = os.path.join(settings.ROOT, 'code')
        pre_name = '/' + str(exercise.id) + '_' + str(submit.id)
        code_filepath = os.path.join(code_path, 'code') + pre_name + '.c'
        f = open(code_filepath, 'w')
        f.write(code)
        f.close()
        data['status'] = True

        exe = os.path.join(code_path, 'exe') + pre_name

        input_file = os.path.join(code_path, 'input') + '/' + str(exercise.id) + '.input'
        output_file = os.path.join(code_path, 'output') + pre_name + '.output'
        err_file = os.path.join(code_path, 'error') + pre_name + '.error'

        command = 'gcc ' + code_filepath + ' -o ' + exe
        #make_result = os.popen(command).read()
        make_result = commands.getoutput(command)
        #替换掉路径
        make_result = make_result.replace(code_path, '')
        #print repr(make_result)
        if make_result:
            submit.mem = 0
            submit.status = 1
            stderr = open(err_file, 'w')
            stderr.write(str(make_result))
            stderr.close()
            pass
        else:
            stdin = open(input_file, 'r')
            stdout = open(output_file, 'w')
            stderr = open(err_file, 'w')
            result = run.exe_main(exe, stdin, stdout, stderr)
            stdin.close()
            stdout.close()
            stderr.close()
            submit.mem = result['mem']
            submit.cpu_time = result['cpu']
            run_result = result['result']
            #判断执行结果是否成功
            if run_result != "OK":
                submit.status = 4
            else:
                f = open(output_file, 'r')
                output_result = f.read()
                if output_result == exercise.output_text:
                    submit.status = 3
                    exercise.success_submit += 1
                    user.total.success_submit += 1
                else:
                    submit.status = 2
            f.close()
        submit.save()
        user.total.save()
        exercise.save()
        return HttpResponse(json.dumps(data), content_type="application/json")
