from django.shortcuts import render
from .serializers.students_serializers import StudentSerializer
from .models import Student
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class StudentListView(generics.ListAPIView):
    """
    List all students.

    This endpoint retrieves a list of all students in the system. Each student includes their associated person details. It requires that the user is authenticated to access this endpoint.

    **Response:**
    - Returns a list of students, including details such as the student ID, code, and associated person information.


    """
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
