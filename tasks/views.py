from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from tasks.models import Task


@login_required
def index(request):
    """View function for the home page of the site."""
    num_tasks = Task.objects.all().count()
    num_workers = User.objects.all().count()

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
    }
    return render(
        request,
        "tasks/index.html",
        context=context
    )