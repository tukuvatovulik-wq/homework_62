from django import forms

from .models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["start_date", "end_date", "name", "description"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "short_description",
            "description",
            "status",
            "task_type",
            "result",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Название задачи"}),
            "short_description": forms.TextInput(
                attrs={"placeholder": "Краткое описание"}
            ),
            "description": forms.Textarea(attrs={"rows": 5}),
            "status": forms.Select(),
            "task_type": forms.Select(),
            "result": forms.Select(),
        }
