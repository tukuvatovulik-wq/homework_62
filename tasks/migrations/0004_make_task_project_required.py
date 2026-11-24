from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("tasks", "0003_assign_existing_tasks_to_project")]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="tasks.project",
                verbose_name="Проект",
            ),
        ),
    ]
