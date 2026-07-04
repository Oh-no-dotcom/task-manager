from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone

from tasks.models import Task, TaskType, Position

TASKS_URL = reverse_lazy("tasks:task-list")


class PublicTaskTest(TestCase):
    def test_login_required(self):
        response = self.client.get(TASKS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="John",
            password="test123",
            position=self.position,
        )
        self.client.force_login(self.worker)

    def test_retrieve_tasks(self):
        Task.objects.create(
            name="Test Task One",
            deadline=timezone.now(),
            task_type=self.task_type,
        )
        Task.objects.create(
            name="Test Task Two",
            deadline=timezone.now(),
            task_type=self.task_type,
        )
        response = self.client.get(TASKS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_list.html")
        tasks = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks),
        )

    def test_search_tasks(self):
        Task.objects.create(
            name="Test Task One",
            deadline=timezone.now(),
            task_type=self.task_type,
        )
        Task.objects.create(
            name="Test Task Two",
            deadline=timezone.now(),
            task_type=self.task_type,
        )
        response = self.client.get(TASKS_URL, {"name": "Test Task One"})
        tasks = response.context["task_list"]
        expected = Task.objects.filter(name__icontains="Test Task One")
        self.assertEqual(list(tasks), list(expected))
        self.assertTemplateUsed(response, "tasks/task_list.html")
        self.assertEqual(len(tasks), 1)
