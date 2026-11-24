from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, UpdateView

from tasks.forms import TaskForm
from tasks.models import Task
from tasks.permissions import ProjectTaskRoleMixin, ProjectTaskDeleteRoleMixin


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False).select_related(
            "project", "task_type", "result"
        )


class TaskUpdateView(ProjectTaskRoleMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.object.project
        return context

    def get_success_url(self):
        return reverse("tasks:detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(ProjectTaskDeleteRoleMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)

    def get_success_url(self):
        return reverse("tasks:project_detail", kwargs={"pk": self.object.project_id})

    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.save(update_fields=["is_deleted"])
        return HttpResponseRedirect(self.get_success_url())
