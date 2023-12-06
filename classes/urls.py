# urls.py

from django.urls import path
from .views import MyClassListView, CourseListView, PDFFileListView, UploadPDFFileView, HomeView, AddClassView, AddCourseView, DeleteClassView, DeleteCourseView, DeletePDFFileView

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('class/all_classes', MyClassListView.as_view(), name='class_list'),
    path('class/add_class/', AddClassView.as_view(), name='add_class'),
    path('class/<int:class_id>/delete/', DeleteClassView.as_view(), name='delete_class'),
    path('class/<int:class_id>/all_courses/', CourseListView.as_view(), name='course_list'),
    path('class/<int:class_id>/add_course/', AddCourseView.as_view(), name='add_course'),
    path('class/<int:class_id>/course/<int:course_id>/delete/', DeleteCourseView.as_view(), name='delete_course'),
    path('class/<int:class_id>/course/<int:course_id>/all_pdfs/', PDFFileListView.as_view(), name='pdf_list'),
    path('class/<int:class_id>/course/<int:course_id>/pdf/<int:pdf_id>/delete/', DeletePDFFileView.as_view(), name='delete_pdf_file'),
    path('class/<int:class_id>/courses/<int:course_id>/upload-pdf/', UploadPDFFileView.as_view(), name='upload_pdf_file'),
]