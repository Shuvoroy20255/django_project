from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course
from enrollments.models import Enrollment
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

# View to display all courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# View to display a specific course's details
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    
    return render(request, 'courses/course_detail.html', {
        'course': course, 
        'is_enrolled': is_enrolled
    })

# View to enroll in a course (requires login)
@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        Enrollment.objects.create(student=request.user, course=course)
    return redirect('course_detail', pk=pk)