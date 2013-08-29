
from django.contrib import admin
from stepbystep.models import Course


class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CourseAdmin)
