from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Worker


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
    name = forms.CharField(
        max_length=64,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
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
