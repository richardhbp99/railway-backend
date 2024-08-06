from django.urls import path
from Subjects import views

urlpatterns = [
    path('list_subjects/', views.SubjectListView.as_view(), name='get-subjects'),
    path('list-pensum/',views.PensumListViews.as_view(),name='get-pensum'),
    path('create-enrollment',views.EnrollmentCreateViews.as_view(),name='create-enrollment'),
    path('students/subjets/<int:student_id>/',views.StudentEnrollmentsList.as_view(), name='student-enrollments-list'),
    path('students/approved-subjects/<int:student_id>/',views.StudentApprovedSubjectsList.as_view(), name='student-approved-subjects-list'),
    path('students/failed-subjects/<int:student_id>/', views.StudentFailedSubjectsList.as_view(), name='student-failed-subjects'),
    path('subjects/update-grades/<int:id_subject>/<int:id_student>/', views.GradeUpdateView.as_view(), name='update-grades'),
    path('grades/<int:subject_id>/', views.SubjectEnrollmentGradeView.as_view(), name='subject-enrollment-grades'),
]
