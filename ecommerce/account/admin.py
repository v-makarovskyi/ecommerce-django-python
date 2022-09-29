from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Address, Customer


class MyUserManager(UserAdmin):
    model = Customer

    list_display = ('id', 'user_name', 'email', 'mobile', 'is_active', 'is_staff')
    ordering = ("id",)
    fieldsets = (
        (None, {'fields' : ('email', 'user_name', 'mobile', 'password')}),
        ('Разрешения', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'email', 'mobile', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )


    


admin.site.register(Customer, MyUserManager)
admin.site.register(Address)
