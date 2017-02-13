from django import forms

from .models import Event


class EventForm(forms.Form):

    name = forms.CharField(label="Summary", max_length=200,
                           widget=forms.TextInput(attrs={'placeholder': 'Short summary'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Date',  'id': 'datepicker'}))
    who = forms.CharField(max_length=200,
                          widget=forms.DateInput(attrs={'placeholder': 'Who did that?', 'id': 'autocomp_who'}))
    function = forms.CharField(max_length=200,
                               widget=forms.DateInput(attrs={'placeholder': 'Position at the time', 'id': 'autocomp_function'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Tell us more about it...'}))




