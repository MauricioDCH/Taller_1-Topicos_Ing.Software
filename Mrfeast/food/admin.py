from django.contrib import admin
from .models import Menu
from user.models import CustomUser
# Register your models here.
admin.site.register(Menu)
admin.site.register(CustomUser)