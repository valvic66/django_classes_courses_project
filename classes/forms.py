# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import PDFFile, MyClass, Course

class PDFFileForm(forms.ModelForm):
  class Meta:
    model = PDFFile
    fields = ['title', 'file', 'course']

class AddClassForm(forms.ModelForm):
  class Meta:
    model = MyClass
    fields = ['name']

class AddCourse(forms.ModelForm):
  class Meta:
    model = Course
    fields = ['title', 'my_class']

class RegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate', 'placeholder': 'Username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

  class Meta:
    model = User
    fields = ['username', 'password']