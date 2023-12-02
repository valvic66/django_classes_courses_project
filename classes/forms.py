# forms.py

from django import forms
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