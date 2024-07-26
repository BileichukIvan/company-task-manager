from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from manager.models import Team
from manager.forms import (
    TeamForm,
    TeamSearchForm,
)


class TeamsListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamsListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = TeamSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Team.objects.all()
        form = TeamSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


class TeamCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    permission_required = "manager.view_team"
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("manager:team-list")


class TeamUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    permission_required = "manager.view_team"
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("manager:team-list")


class TeamDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    permission_required = "manager.view_team"
    model = Team
    success_url = reverse_lazy("manager:team-list")
