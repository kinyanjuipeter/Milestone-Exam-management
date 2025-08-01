from django.urls import path
from . import views
from .views import campus_select, home

app_name = 'exams'

urlpatterns = [
    path('', campus_select, name='campus_select'),
    path('home/', home, name='home'),
    path('enter-marks/', views.enter_marks, name='enter_marks'),
    path('view-records/', views.view_records, name='view_records'),
    path('update-record/<int:record_id>/', views.update_record, name='update_record'),
    path('delete-record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('manage-units/', views.manage_units, name='manage_units'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('download-report/', views.download_report, name='download_report'),
    path('pass-list/', views.pass_list, name='pass_list'),
    path('download-pass-list/', views.download_pass_list, name='download_pass_list'),
    path('records/download/', views.download_records_word, name='download_records_word'),
    path('update-student/<int:student_id>/', views.update_student, name='update_student'),
    path('enter-marks-per-student/', views.enter_marks_per_student, name='enter_marks_per_student'),
    path('manage-campus-passwords/', views.manage_campus_passwords, name='manage_campus_passwords'),
] 