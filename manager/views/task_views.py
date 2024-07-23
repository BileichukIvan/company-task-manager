from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from manager.models import Task, Project
from manager.forms import TaskForm, TaskSearchForm


@login_required
def index(request):
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
        query = self.request.GET.get("query", "")
        show_my_tasks = self.request.GET.get("show_my_tasks", "")

        context["search_form"] = TaskSearchForm(
            initial={"query": query, "show_my_tasks": show_my_tasks}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data.get("query")
            show_my_tasks = form.cleaned_data.get("show_my_tasks")

            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query)
                    | Q(project__name__icontains=query)
                )

            if show_my_tasks:
                queryset = queryset.filter(
                    assigned=self.request.user
                )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        user = self.request.user
        context["can_complete"] = (
            not task.is_completed
            and (user in task.assigned.all() or user.is_superuser)
        )
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")

    def form_valid(self, form):
        response = super().form_valid(form)

        assigned_workers = form.cleaned_data.get("assigned", [])
        if assigned_workers:
            self.object.assigned.set(assigned_workers)

        return response


class TaskCompleteView(LoginRequiredMixin, generic.View):
    @staticmethod
    def post(request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user in task.assigned.all() or request.user.is_superuser:
            task.is_completed = True
            task.save()
        return redirect("manager:task-detail", pk=pk)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")


class TaskDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    permission_required = "manager.view_task"
    model = Task
    success_url = reverse_lazy("manager:task-list")
