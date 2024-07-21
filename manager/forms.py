from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Task,
    Worker,
    Team
)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name", "description", "deadline", "is_completed",
            "priority", "task_type", "assigned", "tags", "project"
        ]
        widgets = {
            "assigned": forms.CheckboxSelectMultiple,
            "tags": forms.CheckboxSelectMultiple,
        }


class TaskSearchForm(forms.Form):
    query = forms.CharField(
        max_length=64,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Task or project"
            }
        )
    )
    show_my_tasks = forms.BooleanField(
        required=False,
        label="Show my tasks"
    )


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=64,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )
    )


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "members", "project"]
        widgets = {
            "members": forms.CheckboxSelectMultiple,
            "project": forms.CheckboxSelectMultiple,
        }
