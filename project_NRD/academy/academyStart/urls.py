from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('courses-list/', CoursesListView.as_view(), name="courses_list"),
    path('course/<int:pk>/', CourseDetailView.as_view(), name="course_details"),
    path('my-courses/', my_registered_courses, name="my_registered_courses"),
    path('course/withdraw/<int:course_id>/', WithdrawFromCourseView.as_view(), name='withdraw_from_course'),
    path('courses/category/<int:category_id>/', CoursesByCategoryView.as_view(), name='courses_by_category'),
    ]
