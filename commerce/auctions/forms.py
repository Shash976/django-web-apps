from django import forms
from .models import *

class NewListingForm(forms.Form):
    listing_title=forms.CharField(label="Enter Title")
    starting_price = forms.IntegerField(label="Starting Price: $")
    description=forms.CharField(widget=forms.Textarea, label="Add Description")
    image = forms.ImageField(required=False)

class NewCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="Write Comment")