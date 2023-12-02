# forms.py

from django import forms
from .models import PDFFile
from .models import MyClass

class PDFFileForm(forms.ModelForm):
  class Meta:
    model = PDFFile
    fields = ['title', 'file', 'course']

class AddClassForm(forms.ModelForm):
  class Meta:
    model = MyClass
    fields = ['name']
