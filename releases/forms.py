from django import forms
from .models import Component


class UploadFileForm(forms.Form):
    component = forms.ChoiceField(choices=[(int(x.id), x.name) for x in Component.objects.all()])
    title = forms.CharField(max_length=200)
    notes = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'rows': 5}))
    file = forms.FileField()