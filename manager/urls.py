from django.urls import path

from .views import (
    index,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerDeleteView,
    WorkerUpdateView,
    TeamsListView,
)

urlpatterns = [
    path(
        "",
        index,
        name="index"
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list",
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/delete<int:pk>/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path(
        "teams/",
        TeamsListView.as_view(),
        name="team-list",
    ),
]

app_name = "manager"
