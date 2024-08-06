from django.urls import path
from Teachers import views


urlpatterns = [
    path('subjects/<int:teacher_id>/', views.TeacherAssignedSubjectsList.as_view(), name='teacher-assigned-subjects-list'),
    path('subjects/students/<int:subject_id>/', views.SubjectStudentsList.as_view(), name='subject-students-list'),
    

]