from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from tasks.forms import (
    TaskCreationForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskTypeCreateForm,
    PositionCreateForm,
    TaskSearchForm,
    WorkerSearchForm,
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

    def get_context_data(
            self,
            *,
            object_list=None,
            **kwargs
    ):
        context = super(
            TaskListView,
            self
        ).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context


    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

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

    def get_queryset(self):
        return (
            Task.objects
            .select_related("task_type")
            .prefetch_related(
                Prefetch(
                    "assignees",
                    queryset=Worker.objects.select_related(
                        "position"
                    ),
                )
            )
        )


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(
            self,
            *,
            object_list=None,
            **kwargs
    ):
        context = super(
            WorkerListView,
            self
        ).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context


    def get_queryset(self):
        queryset = (
            Worker.objects.
            select_related("position").
            annotate(task_count=Count("tasks")
        ))

        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


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


    def get_queryset(self):
        return (
            Worker.
            objects.
            select_related("position")
        )


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
    template_name = "tasks/type_task_list.html"
    context_object_name = "type_task_list"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    template_name = "tasks/type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    template_name = "tasks/type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionCreateForm
    template_name = "tasks/position_form.html"
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionCreateForm
    template_name = "tasks/position_form.html"
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:position-list")
