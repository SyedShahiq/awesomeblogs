from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean_username(self,*args,**kwargs):
    # 	title = self.cleaned_data.get("username")
    # 	if "abc" in title:
    # 		return title
    # 	else:
    # 		raise forms.ValidationError('This is not a valid username')
