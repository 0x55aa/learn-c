
from django.contrib import admin
from exercise.models import Exercise, Submit


class ExerciseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Exercise, ExerciseAdmin)


class SubmitAdmin(admin.ModelAdmin):
    pass
admin.site.register(Submit, SubmitAdmin)
