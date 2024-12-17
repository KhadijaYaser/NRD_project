from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView,DetailView
from .models import *
from django.contrib import messages
from django.views import View

# Create your views here.
class HomeView(ListView):
    model = Category
    template_name = 'home.html'


class CoursesListView(ListView):
    model = Course
    template_name = 'courses_list.html'
    paginate_by = 10

class CoursesByCategoryView(ListView):
    model = Course
    template_name = 'catagory_courses_list.html'
    paginate_by = 10

    def get_queryset(self):
        category_id = self.kwargs.get('category_id') 
        category = get_object_or_404(Category, id=category_id)
        
        return Course.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        course = self.object

        context['is_registered'] = user.is_authenticated and Registration.objects.filter(course=course, user=user).exists()
        context['can_register'] = course.status == 'open'
        return context

    def post(self, request, *args, **kwargs):
        course = self.get_object()

        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to register for a course.")
            return redirect('login')

        if course.status == 'open':
            registration, created = Registration.objects.get_or_create(user=request.user, course=course)
            if created:
                course.total_students += 1
                course.save()
                messages.success(request, "You have successfully registered for the course.")
            else:
                messages.warning(request, "You are already registered for this course.")
        else:
            messages.error(request, "Registration is closed for this course.")

        return redirect('course_details', pk=course.pk)


def my_registered_courses(request):
    if not request.user.is_authenticated:
        return redirect('login')

    registered_courses = Registration.objects.filter(user=request.user)

    return render(request, 'my_registered_courses.html', {
        'registered_courses': registered_courses
    })
    
    
class WithdrawFromCourseView(View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        registration = get_object_or_404(Registration, user=request.user, course=course)
        registration.withdraw()

        course.total_students = course.registrations.count()
        course.save()

        messages.success(request, "You have successfully withdrawn from the course.")
        return redirect('course_details', pk=course.pk)
    



    