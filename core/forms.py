from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'short_description', 'content', 'image', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'panel-input', 'placeholder': 'Yazı Başlığı'}),
            'short_description': forms.Textarea(attrs={'class': 'panel-input', 'rows': 2, 'placeholder': 'Önizleme metni...'}),
            'content': forms.Textarea(attrs={'class': 'panel-input', 'rows': 10, 'placeholder': 'Blog içeriğini buraya yazın...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'panel-checkbox'}),
        }