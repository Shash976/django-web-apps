from email import contentmanager
from django import forms


class NewEntryForm(forms.Form):
    title=forms.CharField(max_length=50)
    content=forms.CharField(widget=forms.Textarea, label="Create New Page")
