from django import forms


class Login(forms.Form):
    username = forms.CharField(label="Username",)
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password")
