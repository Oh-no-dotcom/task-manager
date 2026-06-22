from django import forms
from .models import Task


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
            "assignees": forms.SelectMultiple(
                attrs={"class": "form-select"}
            ),
        }
