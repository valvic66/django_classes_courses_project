# views.py

from django.views.generic import ListView
from .models import MyClass, Course, PDFFile

from django.shortcuts import render, redirect
from django.views import View
from .models import PDFFile
from .forms import PDFFileForm

class MyClassListView(ListView):
    model = MyClass
    template_name = 'class_list.html'
    context_object_name = 'classes'

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        return Course.objects.filter(my_class__id=class_id)

class PDFFileListView(ListView):
    model = PDFFile
    template_name = 'pdf_list.html'
    context_object_name = 'pdf_files'

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return PDFFile.objects.filter(course__id=course_id)

class UploadPDFFileView(View):
    template_name = 'upload_pdf_file.html'

    def get(self, request, course_id):
        form = PDFFileForm(initial={'course': course_id})
        return render(request, self.template_name, {'form': form})

    def post(self, request, course_id):
        form = PDFFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list', course_id=course_id)
        return render(request, self.template_name, {'form': form})