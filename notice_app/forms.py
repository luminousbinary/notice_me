from dataclasses import field
from importlib.resources import contents
from tkinter.ttk import Style
from django import forms
from pkg_resources import require 
# from django.forms import Form
from .models import Comment, PostModel #Student





class PostModelForm(forms.ModelForm):
    required_css_class = 'required-field'

    # content = forms.CharField(
    #     widget=forms.Textarea(attrs={'rows': 4, 'class': 'col-md-12', 'style': 'display:block;',}))
    #     # forms.Textarea
    class Meta:
        model = PostModel
        fields = ('title', 'content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'rows': 4, 'class': 'col-md-12', 'style': 'display:block;',})
        self.fields['content'].widget.attrs.update({'rows': 4, 'class': 'col-md-12', 'style': 'display:block;',})


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('title', 'content')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'rows': 4, 'class': 'col-md-12', 'style': 'display:block;',})
        self.fields['content'].widget.attrs.update({'rows': 4, 'class': 'col-md-12', 'style': 'display:block;',})


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Add comment here....'}))

    class Meta:
        model = Comment
        fields = ('content',)
