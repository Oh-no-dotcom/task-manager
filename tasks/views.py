from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from tasks.forms import (
    TaskCreationForm,
    WorkerCreationForm,
    WorkerUpdateForm,
)
from tasks.models import (
    Task,
    Worker,
    TaskType,
    Position
)


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
    task_list = Task.objects.filter(
        is_completed=False
    ).order_by(
        "deadline"
    )[:10]

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overdue_tasks": overdue_tasks,
        "task_list": task_list,
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


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "tasks/confirm_delete.html"


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(
            self,
            *,
            object_list=None,
            **kwargs
    ):
        context = super(
            WorkerDetailView,
            self
        ).get_context_data(**kwargs)

        worker = self.object

        context["tasks"] = worker.tasks.filter(
            is_completed=False
        ).order_by(
            "deadline"
        )[:5]

        context["completed_tasks_count"] = worker.tasks.filter(
            is_completed=True
        ).count()

        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")
    template_name = "tasks/confirm_delete.html"


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5
