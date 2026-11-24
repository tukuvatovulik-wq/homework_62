from django.contrib import admin

from .models import Project, Task, TaskResult, TaskType


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date")
    search_fields = ("name", "description")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "status", "task_type", "result")
    list_filter = ("status", "task_type", "result", "project")
    search_fields = ("title", "short_description")
    exclude = ("is_deleted",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_deleted=False)
