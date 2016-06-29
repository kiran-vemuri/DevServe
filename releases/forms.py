from django import forms


class BinaryUploadForm(forms.Form):
    binary = forms.FileField(label="Select a file to upload")
