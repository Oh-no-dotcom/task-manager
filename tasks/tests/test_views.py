from django.test import TestCase
from django.urls import reverse_lazy

TASKS_URL = reverse_lazy("tasks:task-list")


class PublicTaskTests(TestCase):
    def test_login_required(self):
        response = self.client.get(TASKS_URL)
        self.assertNotEqual(response.status_code, 200)

