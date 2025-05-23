from django.contrib import admin
from dashboard.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "tc", "is_admin", "is_superuser", "is_active"]
    list_filter = ["is_admin", "is_superuser", "is_active"]  # Removed is_staff
    search_fields = ["email", "name"]
    ordering = ["email"]
    readonly_fields = ["id"]

    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal Info", {"fields": ["name", "tc"]}),
        ("Permissions", {
            "fields": ["is_active", "is_admin", "is_superuser", "groups", "user_permissions"],
        }),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2"],
            },
        ),
    ]

    filter_horizontal = ["groups", "user_permissions"]


# Register the custom admin
admin.site.register(User, UserModelAdmin)

# # Optional: Customize admin panel branding
# admin.site.site_header = "Dashboard Admin"
# admin.site.site_title = "Dashboard Admin Portal"
# admin.site.index_title = "Welcome to the Dashboard Administration"
