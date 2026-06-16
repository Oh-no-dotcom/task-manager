from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tasks.models import Task


@login_required
def index(request):
    """View function for the home page of the site."""
    num_tasks = Task.objects.all().count()
    num_workers = get_user_model().objects.all().count()

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
    }
    return render(
        request,
        "tasks/index.html",
        context=context
    )