from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Worker,
    Task,
    Project,
    TaskType,
    Tag,
    Position,
)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    search_fields = ("username",)
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                        "task_completed",
                        "tasks_not_completed"
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("is_completed",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(TaskType)
admin.site.register(Tag)
admin.site.register(Position)
