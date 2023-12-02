# urls.py

from django.urls import path
from .views import MyClassListView, CourseListView, PDFFileListView, UploadPDFFileView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('class/all_classes', MyClassListView.as_view(), name='class_list'),
    path('class/<int:class_id>/all_courses/', CourseListView.as_view(), name='course_list'),
    path('class/<int:class_id>/course/<int:course_id>/all_pdfs/', PDFFileListView.as_view(), name='pdf_list'),
    path('class/<int:class_id>/courses/<int:course_id>/upload-pdf/', UploadPDFFileView.as_view(), name='upload_pdf_file'),
]