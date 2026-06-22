from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from tasks.form import TaskCreationForm
from tasks.models import Task, Worker, TaskType, Position


@login_required
def index(request):
    """View function for the home page of the site."""
    num_tasks = Task.objects.all().count()
    num_workers = get_user_model().objects.all().count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    in_progress_tasks = Task.objects.filter(
        is_completed=False
    ).count()
    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now(),
        is_completed=False
    ).count()

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overdue_tasks": overdue_tasks,
    }
    return render(
        request,
        "tasks/index.html",
        context=context
    )


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreationForm


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5
