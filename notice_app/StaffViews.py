from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.template import RequestContext
# from django.core.urlresolvers import reverse 
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.shortcuts import render, get_object_or_404
# from .forms import SolutionForm, AssignmentForm,SolCreditForm
# from .models import Assignment, Solution
from django.urls import reverse
# from .forms import AssignmentForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from notice_app.models import CustomUser, PostModel,  Staff, Department, Course, Student,  SessionYearModel #, Attendance # AttendanceReport
from .forms import PostModelForm, PostUpdateForm, CommentForm


def staff_home(request):
    
#     # Fetching All Students under Staff

#     subjects = Subjects.objects.filter(id=request.user.id)
#     course_id_list = []
#     # for subject in subjects:
#     #     course = Courses.objects.get(id=subject.course_id.id)
#     #     course_id_list.append(course.id)
    
#     final_course = []
#     # Removing Duplicate Course Id
#     for course_id in course_id_list:
#         if course_id not in final_course:
#             final_course.append(course_id)
    
#     # students_count = Students.objects.filter(course_id__in=final_course).count()
#     subject_count = subjects.count()

#    

    posts = PostModel.objects.all()
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('staff_home')
    else:
        form = PostModelForm()
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, "staff_template/staff_home_template.html", context)

 
def post_detail(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('post_detail', pk=post.id)
    else:
        c_form = CommentForm()
    context = {
        'post': post,
        'c_form': c_form,
    }
    return render(request, 'staff_template/post_detail.html', context)

def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'staff_template/post_edit.html', context)



def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('staff_home')
    context = {
        'post': post
    }
    return render(request, 'staff_template/post_delete.html', context)



# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    intake_id = request.POST.get("intake")
    subject_id = request.POST.get("subject")

    print(subject_id)
    department = Departments.objects.get(id = department_id)
    # intake = Intakes.objects.get(id = intake_id)
    # subject = Subjects.objects.get(id = subject_id)
    students = Students.objects.filter(department=department).filter(intake=intake)# .filter(subject=subject)
    
    context = {
        'department': department,
        # 'intake': intake,
        'students': students,
        # 'subject' : subject,
    }
    
    
    return render(request, "staff_template/get_students.html", context)

    # return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staff.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staff.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')


