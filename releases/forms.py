from django import forms


class ReleaseUploadForm(forms.Form):
    name = forms.CharField(max_length=200)
    file = forms.FileField()
