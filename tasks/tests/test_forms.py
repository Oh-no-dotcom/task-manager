from django.test import TestCase

from tasks.forms import WorkerCreationForm
from tasks.models import Position


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
