
from django.urls import path, include

from . import views
from .import AdminViews, StaffViews, StudentViews #, ParentViews


urlpatterns = [
    path('', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', AdminViews.admin_home, name="admin_home"),

    # admin post
    path('post_detail/<int:pk>/', AdminViews.post_detail, name='admin_post_detail'),
    path('post_edit/<int:pk>/', AdminViews.post_edit, name='admin_post_edit'),
    path('post_delete/<int:pk>/', AdminViews.post_delete, name='admin_post_delete'),

    # Admin Staff
    path('add_staff/', AdminViews.add_staff, name="add_staff"),
    path('add_staff_save/', AdminViews.add_staff_save, name="add_staff_save"),
    path('manage_staff/', AdminViews.manage_staff, name="manage_staff"),
    path('edit_staff/<staff_id>/', AdminViews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', AdminViews.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/', AdminViews.delete_staff, name="delete_staff"),

    # admin department
    path('add_department/', AdminViews.add_department, name="add_department"),
    path('add_department_save/', AdminViews.add_department_save, name="add_department_save"),
    path('manage_department/', AdminViews.manage_department, name="manage_department"),
    path('edit_department/<department_id>/', AdminViews.edit_department, name="edit_department"),
    path('edit_department_save/', AdminViews.edit_department_save, name="edit_department_save"),
    path('delete_department/<department_id>/', AdminViews.delete_department, name="delete_department"),

    # admin course
    path('add_course/', AdminViews.add_course, name="add_course"),
    path('add_course_save/', AdminViews.add_course_save, name="add_course_save"),
    path('manage_course/', AdminViews.manage_course, name="manage_course"),
    path('edit_course/<course_id>/', AdminViews.edit_course, name="edit_course"),
    path('edit_course_save/', AdminViews.edit_course_save, name="edit_course_save"),
    path('delete_course/<course_id>/', AdminViews.delete_course, name="delete_course"),

    # admin session
    path('manage_session/', AdminViews.manage_session, name="manage_session"),
    path('add_session/', AdminViews.add_session, name="add_session"),
    path('add_session_save/', AdminViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', AdminViews.edit_session, name="edit_session"),
    path('edit_session_save/', AdminViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', AdminViews.delete_session, name="delete_session"),

    # admin student
    path('add_student/', AdminViews.add_student, name="add_student"),
    path('add_student_save/', AdminViews.add_student_save, name="add_student_save"),
    path('manage_student/', AdminViews.manage_student, name="manage_student"),
    path('edit_student/<student_id>/', AdminViews.edit_student, name="edit_student"),
    path('edit_student_save/', AdminViews.edit_student_save, name="edit_student_save"),
    path('delete_student/<student_id>/', AdminViews.delete_student, name="delete_student"),
    path('check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),
    path('admin_profile/', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', AdminViews.admin_profile_update, name="admin_profile_update"),
    
# ------------------------------------------------------------------------------------------------------------

    # URLS for Staff
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    path('get_students/', StaffViews.get_students, name="get_students"),
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"),

    path('stf_post_detail/<int:pk>/', StaffViews.post_detail, name='post_detail'),
    path('stf_post_edit/<int:pk>/', StaffViews.post_edit, name='post_edit'),
    path('stf_post_delete/<int:pk>/', StaffViews.post_delete, name='post_delete'),

    path('get_students_admin/', AdminViews.get_student, name="get_students_admin"),
    

# --------------------------------------------------------------------------------------------------------------
    

    # URSL for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    
    path('st_post_detail/<int:pk>/', StudentViews.post_detail, name='student_post_detail'),

# ----------------------------------------------------------------------------------------------------------------

]
