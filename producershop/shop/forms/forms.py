from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.Form):
    email = forms.CharField(label='Your email', max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    live_contact = forms.BooleanField(
        label='Do you want live session?', required=False)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
