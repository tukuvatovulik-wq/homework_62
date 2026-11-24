from datetime import date

from django.db import migrations


def create_project_and_assign_tasks(apps, schema_editor):
    Project = apps.get_model("tasks", "Project")
    Task = apps.get_model("tasks", "Task")
    if Task.objects.filter(project__isnull=True).exists():
        project, created = Project.objects.get_or_create(
            name="Основной проект",
            defaults={
                "start_date": date(2026, 1, 1),
                "end_date": None,
                "description": "Проект для задач, созданных до добавления проектов.",
            },
        )
        Task.objects.filter(project__isnull=True).update(project_id=project.pk)


def remove_default_project(apps, schema_editor):
    Project = apps.get_model("tasks", "Project")
    Task = apps.get_model("tasks", "Task")
    project = Project.objects.filter(name="Основной проект").first()
    if project:
        Task.objects.filter(project_id=project.pk).update(project_id=None)
        project.delete()


class Migration(migrations.Migration):
    dependencies = [("tasks", "0002_project_and_task_project")]

    operations = [
        migrations.RunPython(
            create_project_and_assign_tasks,
            remove_default_project,
        ),
    ]
