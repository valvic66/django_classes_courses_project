# urls.py

from django.urls import path
from .views import MyClassListView, CourseListView, PDFFileListView, UploadPDFFileView

urlpatterns = [
    path('classes/', MyClassListView.as_view(), name='class_list'),
    path('classes/<int:class_id>/courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:course_id>/pdfs/', PDFFileListView.as_view(), name='pdf_list'),
    path('courses/<int:course_id>/upload-pdf/', UploadPDFFileView.as_view(), name='upload_pdf_file'),
    # ... other URL patterns
]