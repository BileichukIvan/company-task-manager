from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from .models import (
    Task,
    Worker,
    Project,
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

    num_task = Task.objects.count()
    num_worker = Worker.objects.count()
    num_projects = Project.objects.count()

    context = {
        "num_task": num_task,
        "num_worker": num_worker,
        "num_projects": num_projects,
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


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
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


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")
    form_class = WorkerCreationForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("manager:worker-list")
