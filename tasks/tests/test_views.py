from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.utils import timezone

from tasks.models import Task, TaskType, Position

TASKS_URL = reverse_lazy("tasks:task-list")
WORKERS_URL = reverse_lazy("tasks:worker-list")


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


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="John",
            password="test123",
            position=self.position,
        )
        self.client.force_login(self.worker)

    def test_create_worker(self):
        form_data = {
            "username": "Kent",
            "password1": "test12344321",
            "password2": "test12344321",
            "first_name": "Joe",
            "last_name": "Test",
            "position": self.position.id,
        }
        self.client.post(
            reverse("tasks:worker-create"),
            data=form_data,
        )
        new_worker = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_worker.first_name, form_data["first_name"])
        self.assertEqual(new_worker.last_name, form_data["last_name"])
        self.assertEqual(new_worker.position.id, form_data["position"])

    def test_retrieve_workers(self):
        get_user_model().objects.create(
            username="test1234",
            password="test123",
            position=self.position
        )
        get_user_model().objects.create(
            username="test2",
            password="test1234",
            position=self.position
        )
        response = self.client.get(WORKERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_list.html")
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["worker_list"]),
            list(drivers),
        )

    def test_search_worker(self):
        get_user_model().objects.create(
            username="Ivan",
            password="Ivan123",
            position=self.position
        )
        get_user_model().objects.create(
            username="Oleg",
            password="Oleg123",
            position=self.position
        )
        get_user_model().objects.create(
            username="Luke",
            password="Luke123",
            position=self.position
        )
        response = self.client.get(WORKERS_URL, {"username": "Ivan"})
        workers = response.context["worker_list"]
        expected = get_user_model().objects.filter(username__icontains="Ivan")
        self.assertEqual(list(workers), list(expected))
