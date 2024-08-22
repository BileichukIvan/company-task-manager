from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from manager.models import Worker
from manager.forms import (
    WorkerCreationForm,
    WorkerForm,
    WorkerSearchForm,
)


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


class WorkerCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    permission_required = "manager.view_worker"
    model = Worker
    success_url = reverse_lazy("manager:worker-list")
    form_class = WorkerCreationForm


class WorkerDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    permission_required = "manager.view_worker"
    model = Worker
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    permission_required = "manager.view_worker"
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("manager:worker-list")
