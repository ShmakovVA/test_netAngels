from django import forms


class LinkForm(forms.Form):
    url = forms.URLField(help_text='Full link', max_length=1024)


class HashLinkForm(forms.Form):
    hash = forms.CharField(max_length=255)
