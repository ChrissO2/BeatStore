from django import forms


class NameForm(forms.Form):
    email = forms.CharField(label='Your email', max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    live_contact = forms.BooleanField(
        label='Do you want live session?', required=False)
