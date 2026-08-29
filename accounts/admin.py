from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ["email"]
    list_display = ["email", "full_name", "role", "is_active_employee", "is_staff"]
    list_filter = ["role", "is_active_employee", "is_staff"]
    search_fields = ["email", "full_name", "employee_code"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": (
            "full_name", "role", "employee_code", "department",
            "designation", "mobile", "is_active_employee",
        )}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions",
        )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "role", "password1", "password2"),
        }),
    )


admin.site.register(User, CustomUserAdmin)
