from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("tasks", "0004_make_task_project_required")]

    operations = [
        migrations.AddField(
            model_name="task",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name="Удалена"),
        ),
    ]
