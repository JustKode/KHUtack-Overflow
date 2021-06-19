from django import forms
from martor.fields import MartorFormField

class PostForm(forms.Form):
    content = MartorFormField()