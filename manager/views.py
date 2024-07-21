from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render

from .models import (
    Task,
    Worker,
    Project,
    Team,
)
from .forms import (
    TaskForm,
    TaskSearchForm,
    WorkerCreationForm,
    WorkerForm,
    WorkerSearchForm,
)


@login_required
def index(request):
    """View function for the home page of the site."""

    worker = request.user
    assigned_tasks = worker.assigned_tasks.all()
    projects = Project.objects.filter(tasks__in=assigned_tasks).distinct()

    context = {
        "worker": worker,
        "projects": projects
    }

    return render(request, "manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")

    def form_valid(self, form):
        response = super().form_valid(form)

        assigned_workers = form.cleaned_data.get('assigned', [])
        if assigned_workers:
            self.object.assigned.set(assigned_workers)

        return response


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")


class TaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "manager.view_task_delete"
    model = Task
    success_url = reverse_lazy("manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5
    context_object_name = "workers"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")

        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = "manager.view_worker"
    model = Worker
    success_url = reverse_lazy("manager:worker-list")
    form_class = WorkerCreationForm


class WorkerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "manager.view_worker"
    model = Worker
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "manager.view_worker"
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("manager:worker-list")
