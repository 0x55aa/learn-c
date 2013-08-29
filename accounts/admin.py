
from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import Total


class TotalAdmin(admin.ModelAdmin):
    pass
admin.site.register(Total, TotalAdmin)
