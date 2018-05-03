from django import forms
from django.contrib.admin import widgets
from .models import Memo

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ('name', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10})
        }
