from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from ..models import Position
from ..forms import PositionForm


class PositionListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "manager.view_position"
    model = Position


class PositionCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = "manager.view_position"
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("manager:position-list")


class PositionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "manager.view_position"
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("manager:position-list")


class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "manager.view_position"
    model = Position
    success_url = reverse_lazy("manager:position-list")
