from django.urls import path

from .models import Worker, TaskType
from .views import (
    index,
    TaskListView,
    TaskCreateView,
    WorkerListView,
    TaskTypeListView,
    PositionListView,
)

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    ]
