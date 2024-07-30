from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from manager.models import Tag
from manager.forms import TagForm


class TagListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.ListView
):
    permission_required = "manager.view_tag"
    model = Tag


class TagCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    permission_required = "manager.view_tag"
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("manager:tag-list")


class TagUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    permission_required = "manager.view_tag"
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("manager:tag-list")


class TagDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    permission_required = "manager.view_tag"
    model = Tag
    success_url = reverse_lazy("manager:tag-list")
