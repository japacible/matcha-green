from django import forms
import models, datetime

class LoginForm(forms.Form):
	username = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())
	organization = forms.CharField()
