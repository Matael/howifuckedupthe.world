from django import forms

from .models import Event


class EventForm(forms.Form):

    date = forms.DateField(widget=forms.DateInput(attrs={'id': 'datepicker'}))
    name = forms.CharField(max_length=200)
    who = forms.CharField(max_length=200, widget=forms.DateInput(attrs={'id': 'autocomp_who'}))
    description = forms.CharField(widget=forms.Textarea)
    function = forms.CharField(max_length=200, widget=forms.DateInput(attrs={'id': 'autocomp_function'}))




