from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Branch)
admin.site.register(Company)
admin.site.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ...
    )
admin.site.register(Role)