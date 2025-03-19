from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .views import Task


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-input"
        self.fields["username"].widget.attrs["placeholder"] = "type your username..."
        
        self.fields["email"].widget.attrs["class"] = "form-input"
        self.fields["email"].widget.attrs["placeholder"] = "type your email..."
        
        self.fields["password1"].widget.attrs["class"] = "form-input"
        self.fields["password1"].widget.attrs["placeholder"] = "type your password..."
                
        self.fields["password2"].widget.attrs["class"] = "form-input"
        self.fields["password2"].widget.attrs["placeholder"] = "type your password again..."
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
