from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from notice_app.models import CustomUser, PostModel, Comment, Staff, Department, Course, Student,  SessionYearModel #, Attendance # AttendanceReport
from .forms import PostModelForm, PostUpdateForm, CommentForm


def admin_home(request):

    posts = PostModel.objects.all()
    if request.method == 'POST':
        form = PostModelForm(request.POST,)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('admin_home')
    else:
        form = PostModelForm()
    context = {
        'posts': posts,
        'form': form
    }

    return render(request, "admin_template/home_content.html", context)

def post_detail(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('admin_post_detail', pk=post.id)
    else:
        c_form = CommentForm()
    context = {
        'post': post,
        'c_form': c_form,
    }
    return render(request, 'admin_template/post_detail.html', context)

def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('admin_post_detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'admin_template/post_edit.html', context)



def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('admin_home')
    context = {
        'post': post
    }
    return render(request, 'admin_template/post_delete.html', context)

# #staff
def add_staff(request):
    return render(request, "admin_template/add_staff_template.html")

def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = "0123456789mtu"
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staff.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')

def manage_staff(request):
    staffs = Staff.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "admin_template/manage_staff_template.html", context)

def edit_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "admin_template/edit_staff_template.html", context)

def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if password != None and password != "":
                user.set_password(password)
            user.username = username
            user.save()
            
            # INSERTING into Staff Model
            staff_model = Staff.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/'+staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+staff_id)

def delete_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')


# #department
def add_department(request):
    return render(request, "admin_template/add_department_template.html")

def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_department')
    else:
        department = request.POST.get('department')
        try:
            department_model = Department(department_name=department)
            department_model.save()
            messages.success(request, "Department Added Successfully!")
            return redirect('add_department')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('add_department')

def manage_department(request):
    departments = Department.objects.all()
    context = {
        "departments": departments
    }
    return render(request, 'admin_template/manage_department_template.html', context)

def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    context = {
        "department": department,
        "id": department_id
    }
    return render(request, 'admin_template/edit_department_template.html', context)

def edit_department_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department')

        try:
            department = Department.objects.get(id=department_id)
            department.department_name = department_name
            department.save()

            messages.success(request, "department Updated Successfully.")
            return redirect('/edit_department/'+department_id)

        except:
            messages.error(request, "Failed to Update department.")
            return redirect('/edit_department/'+department_id)

def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    try:
        department.delete()
        messages.success(request, "department Deleted Successfully.")
        return redirect('manage_department')
    except:
        messages.error(request, "Failed to Delete department.")
        return redirect('manage_department')

#  #course
def add_course(request):
    departments = Department.objects.all()
    context = {
        "departments":departments,
    }
    return render(request, "admin_template/add_course_template.html", context)

def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course = request.POST.get('course')
        choices = request.POST.get('department')
        # department = Department.objects.filter()
        # try:
        course_model = Course(course_name=course, department_name=Department.objects.get(id=choices))
        course_model.save()
        messages.success(request, "Course Added Successfully!")
        return redirect('add_course')
        # except:
        #     messages.error(request, "Failed to Add Course!")
        #     return redirect('add_course')

def manage_course(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, 'admin_template/manage_course_template.html', context)

def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, 'admin_template/edit_course_template.html', context)

def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')

        try:
            course = Course.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_course/'+course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/'+course_id)

def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')

# #session
def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "admin_template/manage_session_template.html", context)

def add_session(request):
    return render(request, "admin_template/add_session_template.html")

def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")

def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "admin_template/edit_session_template.html", context)

def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)

def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


# #student
def add_student(request):
    departments = Department.objects.all()
    courses = Course.objects.all()
    sessions = SessionYearModel.objects.all()
    context = {
        "departments":departments,
        "courses":courses,
        "sessions":sessions,
    }
    return render(request, 'admin_template/add_student_template.html')

def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_student')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = "mtu123456789"
        
        # course = request.POST.get('course')
        # department = request.POST.get('department')
        # gender = request.POST.get('gender')
        # session = request.POST.get('session')

        user = CustomUser.objects.create_user(username=username, password=password, email=email, 
        last_name=last_name, first_name=first_name,  user_type=3)
        user.save()
        messages.success(request, "student Added Successfully!")
        return redirect('add_student')


def manage_student(request):
    students = Student.objects.all()
    context = {
        "students": students
    }
    return render(request, "admin_template/manage_student_template.html", context)

def edit_student(request, student_id):
    student = Student.objects.get(admin=student_id)
    department = Department.objects.all()
    course = Course.objects.all()
    # sessions = SessionYearModel.objects.all()
    context = {
        # "sessions":sessions
        "department":department,
        "course":course,
        "student": student,
        "student_id": student_id
    }
    return render(request, "admin_template/edit_student_template.html", context)

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        course = request.POST.get('course')
        department = request.POST.get('department')
        intake = request.POST.get('intake')
        gender = request.POST.get('gender')
        session = request.POST.get('session')
        password = request.POST.get('password')


        # try:
        # INSERTING into Customuser Model
        user = CustomUser.objects.get(id=student_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password != None and password != "":
            user.set_password(password)
        user.username = username
        user.save()
        
        # INSERTING into student Model
        print(department)
        student_model = Student.objects.get(admin=student_id)
        student_model.department=Department.objects.get(id=department) 
        student_model.course=Course.objects.get(course_name=course)
        student_model.gender=gender
        student_model.address = address
        student_model.save()

        messages.success(request, "student Updated Successfully.")
        return redirect('/edit_student/'+student_id)

def delete_student(request, student_id):
    student = Student.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete student.")
        return redirect('manage_student')


# The exempts
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'admin_template/admin_profile.html', context)

def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    
def staff_profile(request):
    pass

def student_profile(requtest):
    pass






def view_at(request):
    department = Department.objects.filter()
    context = {
        "department": department,
    }
    return render(request, "admin_template/view_at_template.html", context)

@csrf_exempt
def get_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    intake_id = request.POST.get("intake")
    subject_id = request.POST.get("subject")

    print(subject_id)
    department = Department.objects.get(id = department_id)
    staff = Staff.objects.all()
    student = Student.objects.filter(department=department)
    context = {
        'department': department,
        'student': student,
    }

    return render(request, "admin_template/get_student.html", context)
