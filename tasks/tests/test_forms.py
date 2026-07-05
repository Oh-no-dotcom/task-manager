from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from tasks.forms import WorkerCreationForm, TaskCreationForm, TaskSearchForm
from tasks.models import Position, TaskType


class WorkerCreationFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Developer",
        )

    def test_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": self.position.id
        }

        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskCreationFormTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="Test type",
        )
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="john",
            password="12345",
            position=self.position,
        )

    def test_form_is_valid(self):
        form_data = {
            "name": "Test name",
            "deadline": timezone.now(),
            "task_type": self.task_type.id,
            "priority": "LOW",
            "assignees": [self.worker.id],
        }

        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskSearchFormTest(TestCase):
    def test_search_form_is_valid(self):
        form = TaskSearchForm(data={"name": "test"})
        self.assertTrue(form.is_valid())

    def test_search_form_empty_is_valid(self):
        form = TaskSearchForm(data={})
        self.assertTrue(form.is_valid())

