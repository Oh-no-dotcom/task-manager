from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Task, Worker, TaskType


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control"}
            ),
            "deadline": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "priority": forms.Select(
                attrs={"class": "form-select"}
            ),
            "task_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "assignees": forms.CheckboxSelectMultiple(),
        }


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "position": forms.Select(
                attrs={"class": "form-select"}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update(
            {"class": "form-control"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control"}
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = (
            "username",
            "first_name",
            "last_name",
            "position",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "position": forms.Select(
                attrs={"class": "form-select"}
            ),
        }


class TaskTypeCreateForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            )
        }
