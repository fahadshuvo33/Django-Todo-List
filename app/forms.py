from django import forms
from app.models import Task  # Import the Task model

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name']
