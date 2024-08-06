from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Subjects.serializers.subject_serializers import SubjectSerializer
from Teachers.serializers.teachers_serializers import StudentSubjectSerializer

from Subjects.models import Enrollment, Subject
from Students.models import Student
# Create your views here.


#6. Un profesor puede tener asignadas varias materias
#7. Un profesor puede obtener las lista de materias a las que esta asignado

class TeacherAssignedSubjectsList(generics.ListAPIView):


    """
    List all subjects assigned to a specific teacher.

    This endpoint retrieves a list of subjects that are assigned to a particular teacher. It requires that the user is authenticated to access this endpoint.

    **Parameters:**
    - `teacher_id`: The unique identifier of the teacher whose assigned subjects are being retrieved. This should be provided as a URL parameter.

    **Response:**
    - Returns a list of subjects assigned to the specified teacher. Each subject includes details such as the subject ID, code, name, and any associated prerequisites.
    """
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Obtén el ID del profesor de los parámetros de la URL
        teacher_id = self.kwargs['teacher_id']
        
        # Filtra las materias asignadas al profesor
        return Subject.objects.filter(teacher_id=teacher_id)


#8. Un profesor puede ver la lista de estudiantes de cada una de sus materias

class SubjectStudentsList(generics.ListAPIView):

    """
    List all students enrolled in a specific subject.

    This endpoint retrieves a list of students who are enrolled in a particular subject. It requires that the user is authenticated to access this endpoint.

    **Parameters:**
    - `subject_id`: The unique identifier of the subject whose enrolled students are being retrieved. This should be provided as a URL parameter.

    **Response:**
    - Returns a list of students enrolled in the specified subject. Each student includes details such as the student ID, code, and associated person information.


    """
    serializer_class = StudentSubjectSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
       
        subject_id = self.kwargs['subject_id']
        
       
        student_ids = Enrollment.objects.filter(subject=subject_id).values_list('student', flat=True)
        
       
        return Student.objects.filter(id_student__in=student_ids)
