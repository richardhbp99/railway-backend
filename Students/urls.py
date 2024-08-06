from django.urls import path
from Students import views

urlpatterns = [
    path('list_students/',views.StudentListView.as_view(),name='get-studets'),

]