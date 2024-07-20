from django import forms
from .models import Task


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
