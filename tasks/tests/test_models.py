from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from tasks.models import Task, TaskType, Position


class ModelsTest(TestCase):
    def test_task_str(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(
            name="test",
            deadline=timezone.now(),
            task_type=task_type
        )
        self.assertEqual(str(task), "test")

    def test_position_str(self):
        position = Position.objects.create(name="Developer")

        self.assertEqual(str(position), "Developer")

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Bug")

        self.assertEqual(str(task_type), "Bug")

    def test_worker_str(self):
        position = Position.objects.create(name="Developer")

        worker = get_user_model().objects.create_user(
            username="john_s",
            password="test123",
            position=position,
            first_name="John",
            last_name="Smith",
        )
        self.assertEqual(str(worker), "Developer - john_s(John Smith)")
