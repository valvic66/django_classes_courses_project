# views.py

from django.views.generic import ListView
from .models import MyClass, Course, PDFFile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import PDFFile
from .forms import PDFFileForm, AddClassForm, AddCourse, RegisterForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import login, authenticate, logout
from django.utils.decorators import method_decorator
from django.urls import reverse

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegisterForm()

        return render(request, self.template_name, {'registerform': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login_view')
        
        context = {'registerform': form}

        return render(request, self.template_name, context=context)

@method_decorator(login_required(login_url='login_view'), name='dispatch')    
class LogoutView(View):
    def get(self, request):
        auth.logout(request)

        return redirect('login_view')    

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()

        return render(request, self.template_name, {'loginform': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect('home_view')
            else:
                return render(request, self.template_name, {'loginform': form, 'error': 'Invalid username or password'})

        context = {'loginform': form}

        return render(request, self.template_name, context=context)

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class HomeView(ListView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        # is_admin = request.user.is_staff
        # is_guest = not request.user.is_authenticated

        return render(request, self.template_name,
            # {'is_admin': is_admin, 'is_guest': is_guest}
        )

@method_decorator(login_required(login_url='login_view'), name='dispatch')    
class ContactView(ListView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
@method_decorator(login_required(login_url='login_view'), name='dispatch')
class MyClassListView(ListView):
    model = MyClass
    template_name = 'class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return MyClass.objects.order_by('-created_at')

class AddClassView(View):
    template_name = 'add_class.html'

    def get(self, request):
        form = AddClassForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AddClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')  # Change this to the appropriate URL name
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class DeleteClassView(View):
    def post(self, request, class_id):
        my_class = get_object_or_404(MyClass, id=class_id)

        # Delete associated courses and PDF files
        courses = Course.objects.filter(my_class=my_class)
        for course in courses:
            pdf_files = PDFFile.objects.filter(course=course)
            for pdf_file in pdf_files:
                # Delete the file from the server
                pdf_file.file.delete(save=False)
            course.delete()

        # Now, delete the class
        my_class.delete()

        # Redirect to the classes page or any other appropriate page
        return redirect('class_list')  # Change this to the appropriate URL name

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        return Course.objects.filter(my_class__id=class_id).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_id = self.kwargs['class_id']
        context['class_id'] = class_id
        context['class_name'] = MyClass.objects.get(id=class_id).name
        return context

@method_decorator(login_required(login_url='login_view'), name='dispatch')    
class AddCourseView(View):
    template_name = 'add_course.html'  # Create this template

    def get(self, request, class_id):
        form = AddCourse(initial={'my_class': class_id})
        return render(request, self.template_name, {'form': form, 'class_id': class_id})

    def post(self, request, class_id):
        form = AddCourse(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list', class_id=class_id)
        
        return render(request, self.template_name, {'form': form, 'class_id': class_id})

@method_decorator(login_required(login_url='login_view'), name='dispatch')    
class DeleteCourseView(View):
    def post(self, request, class_id, course_id):
        course = get_object_or_404(Course, id=course_id)

        # Delete associated PDF files
        pdf_files = PDFFile.objects.filter(course=course)
        for pdf_file in pdf_files:
            # Delete the file from the server
            pdf_file.file.delete(save=False)

        # Now, delete the course
        course.delete()

        # Redirect to the course list page or any other appropriate page
        return redirect('course_list', class_id=class_id)  # Change this to the appropriate URL name

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class PDFFileListView(ListView):
    model = PDFFile
    template_name = 'pdf_list.html'
    context_object_name = 'pdf_files'

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return PDFFile.objects.filter(course__id=course_id).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_id = self.kwargs['class_id']
        course_id = self.kwargs['course_id']
        context['class_id'] = class_id
        context['class_name'] = MyClass.objects.get(id=class_id).name
        context['course_id'] = course_id
        context['course_title'] = Course.objects.get(id=course_id).title
        context['form'] = PDFFileForm(initial={'course': course_id})
        return context

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class DeletePDFFileView(View):
    def post(self, request, class_id, course_id, pdf_id):
        pdf_file = get_object_or_404(PDFFile, id=pdf_id)

        # Delete the file from the server
        pdf_file.file.delete(save=False)

        # Now, delete the PDF file record
        pdf_file.delete()

        # Redirect to the PDF list page or any other appropriate page
        return redirect('pdf_list', class_id=class_id, course_id=course_id)    

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class UploadPDFFileView(View):
    template_name = 'upload_pdf_file.html'

    def get(self, request, class_id, course_id):
        form = PDFFileForm(initial={'course': course_id})
        return render(request, self.template_name, {'form': form, 'class_id': class_id, 'course_id': course_id})

    def post(self, request, class_id, course_id):
        form = PDFFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list', class_id=class_id, course_id=course_id)
        return render(request, self.template_name, {'form': form, 'class_id': class_id, 'course_id': course_id})    
