from django.urls import path

from .views.member_views import project_members
from .views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectTaskCreateView,
    ProjectUpdateView,
    TaskDeleteView,
    TaskDetailView,
    TaskUpdateView,
)

app_name = "tasks"

urlpatterns = [
    path("", ProjectListView.as_view(), name="list"),
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("projects/<int:pk>/edit/", ProjectUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path("projects/<int:pk>/members/", project_members, name="project_members"),
    path(
        "projects/<int:project_pk>/tasks/create/",
        ProjectTaskCreateView.as_view(),
        name="task_create",
    ),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="delete"),
]
