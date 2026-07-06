from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Worker, Task, TaskType, Position


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional information", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "position",
                ),
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("task_type",)


admin.site.register(TaskType)


admin.site.register(Position)
