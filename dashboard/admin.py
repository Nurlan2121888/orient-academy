from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm
from .models import Group, Student, Lesson, Attendance


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "teacher",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "is_active",
        "teacher",
    )

    search_fields = (
        "name",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "group",
        "lesson_date",
        "start_time",
        "end_time",
    )

    list_filter = (
        "group",
        "lesson_date",
    )

    search_fields = (
        "title",
        "group__name",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "lesson",
        "student",
        "status",
    )

    list_filter = (
        "status",
        "lesson",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
    )