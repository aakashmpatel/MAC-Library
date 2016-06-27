from django import forms
from libapp.models import Suggestion

class SuggestionForm(forms.ModelForm):
    class Meta:
        model= Suggestion
        fields=['title','pubyr','type','cost','comments']
    choice = [('2','Dvd'),('1','Book')]
    title = forms.CharField(label='Title',max_length=100)
    pubyr = forms.IntegerField(label='Publication Year')
    type = forms.ChoiceField(label='Type',choices = choice,widget=forms.RadioSelect)
    cost = forms.IntegerField(label='Estimated Cost in Dollars')
    comments = forms.CharField(label='Comments')

class SearchlibForm(forms.Form):
    class Meta:
        fields = ['title','author']
    title = forms.CharField(label='Title',max_length=100)
    author = forms.CharField(label='Author')

class LoginForm(forms.Form):
    class Meta:
        fields = ['username','password']

    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput())