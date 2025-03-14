from django.forms import ModelForm

from .views import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
