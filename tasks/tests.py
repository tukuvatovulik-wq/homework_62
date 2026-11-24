from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ProjectForm, TaskForm
from .models import Project, Task, TaskResult, TaskType


class ProjectTaskTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            start_date=date(2026, 1, 1),
            name="Тестовый проект",
            description="Описание тестового проекта.",
        )
        cls.task_type = TaskType.objects.create(name="Баг")
        cls.result = TaskResult.objects.create(name="Исправлено")
        cls.user = get_user_model().objects.create_user(username="tester", password="test-password-123")
        cls.task = Task.objects.create(
            title="Проверить форму",
            short_description="Проверка корректной работы формы.",
            status=Task.Status.NEW,
            task_type=cls.task_type,
            result=cls.result,
            project=cls.project,
        )

    def setUp(self):
        self.client.login(username="tester", password="test-password-123")

    def task_data(self, title="Создать новую задачу"):
        return {
            "title": title,
            "short_description": "Описание новой задачи для проверки.",
            "description": "",
            "status": Task.Status.NEW,
            "task_type": self.task_type.pk,
            "result": self.result.pk,
        }

    def test_project_list_page(self):
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)

    def test_project_search_by_description(self):
        response = self.client.get(reverse("tasks:list"), {"search": "тестового"})
        self.assertContains(response, self.project.name)

    def test_project_search_no_results(self):
        response = self.client.get(reverse("tasks:list"), {"search": "несуществующее"})
        self.assertContains(response, "Проекты не найдены")

    def test_project_detail_contains_tasks(self):
        response = self.client.get(
            reverse("tasks:project_detail", kwargs={"pk": self.project.pk})
        )
        self.assertContains(response, self.task.title)

    def test_project_create_page(self):
        response = self.client.get(reverse("tasks:project_create"))
        self.assertEqual(response.status_code, 200)

    def test_project_form(self):
        form = ProjectForm(data={
            "start_date": "2026-02-01",
            "end_date": "",
            "name": "Новый проект",
            "description": "Описание нового проекта.",
        })
        self.assertTrue(form.is_valid())

    def test_task_create_inside_project(self):
        response = self.client.post(
            reverse("tasks:task_create", kwargs={"project_pk": self.project.pk}),
            self.task_data(),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project.tasks.count(), 2)

    def test_task_form_does_not_contain_project_or_is_deleted(self):
        self.assertNotIn("project", TaskForm().fields)
        self.assertNotIn("is_deleted", TaskForm().fields)

    def test_task_detail_page(self):
        response = self.client.get(
            reverse("tasks:detail", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_task_update_page(self):
        response = self.client.get(
            reverse("tasks:update", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_task_soft_delete(self):
        response = self.client.post(
            reverse("tasks:delete", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_deleted)

    def test_deleted_task_detail_returns_404(self):
        self.task.is_deleted = True
        self.task.save()
        response = self.client.get(
            reverse("tasks:detail", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_deleted_tasks_are_not_in_project(self):
        self.task.is_deleted = True
        self.task.save()
        response = self.client.get(
            reverse("tasks:project_detail", kwargs={"pk": self.project.pk})
        )
        self.assertNotContains(response, self.task.title)


class AuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            start_date=date(2026, 1, 1), name="Auth project", description="Auth test project"
        )
        cls.task_type = TaskType.objects.create(name="Auth type")
        cls.result = TaskResult.objects.create(name="Auth result")
        cls.task = Task.objects.create(
            title="Auth task", short_description="Task for access test",
            status=Task.Status.NEW, task_type=cls.task_type, result=cls.result,
            project=cls.project,
        )
        cls.user = get_user_model().objects.create_user(
            username="tester", password="test-password-123"
        )

    def test_login_page_available(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirected_from_protected_pages(self):
        protected_urls = [
            reverse("tasks:project_create"),
            reverse("tasks:project_update", kwargs={"pk": self.project.pk}),
            reverse("tasks:project_delete", kwargs={"pk": self.project.pk}),
            reverse("tasks:task_create", kwargs={"project_pk": self.project.pk}),
            reverse("tasks:update", kwargs={"pk": self.task.pk}),
            reverse("tasks:delete", kwargs={"pk": self.task.pk}),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_login_and_logout(self):
        response = self.client.post(reverse("login"), {
            "username": "tester", "password": "test-password-123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(reverse("tasks:list")))
        self.assertTrue(self.client.session.get("_auth_user_id"))
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.session.get("_auth_user_id"))


    def test_authenticated_user_can_open_protected_pages(self):
        self.client.login(username="tester", password="test-password-123")
        protected_urls = [
            reverse("tasks:project_create"),
            reverse("tasks:project_update", kwargs={"pk": self.project.pk}),
            reverse("tasks:project_delete", kwargs={"pk": self.project.pk}),
            reverse("tasks:task_create", kwargs={"project_pk": self.project.pk}),
            reverse("tasks:update", kwargs={"pk": self.task.pk}),
            reverse("tasks:delete", kwargs={"pk": self.task.pk}),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_anonymous_cannot_delete_task(self):
        response = self.client.post(reverse("tasks:delete", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_deleted)
