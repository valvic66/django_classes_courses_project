# models.py

from django.db import models
from django.contrib.auth.models import User

class MyClass(models.Model):
  name = models.CharField(max_length=100)
  students = models.ManyToManyField(User, related_name='classes')

  def __str__(self):
    return self.name

class Course(models.Model):
  title = models.CharField(max_length=100)
  my_class = models.ForeignKey(MyClass, on_delete=models.CASCADE, related_name='courses')

  def __str__(self):
    return self.title

class PDFFile(models.Model):
  title = models.CharField(max_length=100)
  file = models.FileField(upload_to='pdfs/')
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='pdf_files')

  def __str__(self):
    return self.title
