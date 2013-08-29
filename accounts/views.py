# coding: utf-8
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.forms import RegisterForm
from accounts.models import Total


class ProfileView(DetailView):
    model = Total
    template_name = "accounts/profile.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_object(self, **kwargs):
        try:
            return Total.objects.get(user=self.request.user)
        except:
            return None


class RegisterView(CreateView):
    model = User
    template_name = "accounts/register.html"
    form_class = RegisterForm

    #用success_url出现函数参数提前调用的情况
    #success_url = reverse('profile')
    def get_success_url(self):
        return reverse('login')
