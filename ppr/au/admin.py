from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, My_card, My_crcard, My_buyes

admin.site.register(User, UserAdmin)
admin.site.register(My_card)
admin.site.register(My_crcard)
admin.site.register(My_buyes)