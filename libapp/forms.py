from django import forms
from libapp.models import Suggestion,User,UserProfile
from libapp.validators import validate_pubyr

class SuggestionForm(forms.ModelForm):
    class Meta:
        model= Suggestion
        fields=['title','pubyr','type','cost','comments']
    choice = [('2','Dvd'),('1','Book')]
    title = forms.CharField(label='Title',max_length=100,widget=forms.TextInput(attrs={'class': "form-control"}))
    pubyr = forms.IntegerField(label='Publication Year',validators=[validate_pubyr],widget=forms.TextInput(attrs={'class': "form-control"}))
    type = forms.ChoiceField(label='Type',choices = choice,widget=forms.RadioSelect())
    cost = forms.IntegerField(label='Estimated Cost in Dollars',widget=forms.TextInput(attrs={'class': "form-control"}))
    comments = forms.CharField(label='Comments',widget=forms.TextInput(attrs={'class': "form-control"}))

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


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fname','lname','username','password','email']

    fname = forms.CharField(label='First Name')
    lname = forms.CharField(label='Last Name')
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']

