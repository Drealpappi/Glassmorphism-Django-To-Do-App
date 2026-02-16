from django import forms
from django.forms import ModelForm
from .models import *
# Create your forms here.
class TaskForm(forms.ModelForm):
    
    forms.CharField(widget= forms.TextInput(attrs= {
        'class': 'form-control',
        'placeholder': 'Add new task',
    }))
    
    class Meta:
        model = Task
        fields = ['title', 'completed']
    