from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Subject,Enrollment,Pensum
from .serializers.subject_serializers import SubjectSerializer
from .serializers.pensum_serializers import PensumSerializer
from .serializers.enrollment_serializers import EnrollmentCreateSerializer,SubjectEstudentsSerializer,SubjectEstudentsapprovedSerializer,SubjectEstudentFailedSerializer,GradeUpdateSerializer,EnrollmentGradeSerializer
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.response import Response
from django.db.models import Avg

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.
class SubjectListView(generics.ListAPIView):

    """
    List all subjects.

    This endpoint retrieves a list of all subjects available in the system. It requires that the user is authenticated to access this endpoint.

    **Response:**
    - Returns a list of subjects, including details such as subject code, name, and associated teacher.

    **Example Request:**
    ```
    GET /api/subjects/
    ```
    """

    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer




class PensumListViews(generics.ListAPIView):


    """
        List all pensums.

        This endpoint retrieves a list of all pensums available in the system. Each pensum includes its associated subjects. It requires that the user is authenticated to access this endpoint.

        **Response:**
        - Returns a list of pensums, including details such as the pensum name, start year, end year, and the subjects associated with each pensum.

        **Example Request:**
        ```
        GET /api/pensums/
    ```
    """

    queryset = Pensum.objects.all()
    serializer_class = PensumSerializer 
    permission_classes = [IsAuthenticated]

#1. Un estudiante se inscribe en una lista de materias
class EnrollmentCreateViews(generics.CreateAPIView):
    """
    Enroll students in all subjects of a given Pensum.

    This endpoint allows the creation of enrollments for all subjects associated with a specified `Pensum`.
    It requires an authenticated user to access.

    """
    queryset = Enrollment.objects.all()
    serializer_class= EnrollmentCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id_pensum': openapi.Schema(type=openapi.TYPE_INTEGER, description='The ID of the Pensum'),
            'student': openapi.Schema(type=openapi.TYPE_INTEGER, description='The ID of the student'),
        },
        required=['id_pensum', 'student']
    ),
    responses={
        201: openapi.Response(
            description='Enrollment created successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'date': openapi.Schema(type=openapi.TYPE_STRING, description='Date of enrollment'),
                        'student': openapi.Schema(type=openapi.TYPE_INTEGER, description='Student ID'),
                        'subject': openapi.Schema(type=openapi.TYPE_INTEGER, description='Subject ID'),
                    }
                )
            )
        ),
        400: 'Bad Request',
        404: 'Not Found'
    }
)
    def post(self, request):
        data_in = request.data

        if  not 'id_pensum' in data_in:
            raise ValidationError("no pensum found")
        
        pensum = Pensum.objects.filter(id_pensum=data_in['id_pensum']).first()
        

        if not pensum:
            raise NotFound("")
        
        subjects = pensum.subjects.all()

 
        data_enrollment=[]
        
        for subject in subjects:
            
            
            data_enrollment.append({
                "date": "2024-08-02",
                "student": data_in['student'],
                "subject": subject.id_subject
                })
        serializer = self.serializer_class(data=data_enrollment,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

#2. Un estudiante puede obtener la lista de materias en las que está inscrito.
class StudentEnrollmentsList(generics.ListAPIView):

    """
    List all subjets for a specific student.

    This endpoint retrieves a list of all enrollments for a given student identified by their ID.
    It requires that the user is authenticated to access this endpoint.
    
    """
    serializer_class = SubjectEstudentsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        
        student_id = self.kwargs['student_id']
       
        return Enrollment.objects.filter(student_id=student_id)
    




#3. Un estudiante aprueba una materia con una nota igual o mayor a 3.0.

#4 Un estudiante puede obtener la lista de sus materias aprobadas y su promediode puntaje general.

class StudentApprovedSubjectsList(generics.ListAPIView):

    """
        List all approved subjects and the average grade for a specific student.

        This endpoint retrieves a list of subjects that a student has passed (i.e., grades 3 or higher) and calculates the average grade for all subjects the student is enrolled in. 

        **Parameters:**
        - `student_id` (int): The ID of the student whose approved subjects and average grade are to be retrieved. This should be provided as a URL path parameter.

        **Response:**
        - Returns an object with two keys:
            - `subjects`: A list of subjects that the student has passed, including subject details.
            - `average`: The average grade of the student across all subjects.
    """
    serializer_class = SubjectEstudentsapprovedSerializer
    permission_classes = [IsAuthenticated]
    def get(self,kwargs,student_id):
       
        student_id = student_id


        enrollments = Enrollment.objects.filter(student=student_id, grade__isnull=False)
        approved = enrollments.filter(grade__gte=3)
      
        subject_ids = approved.values_list('subject_id', flat=True)
        average_grade = enrollments.aggregate(Avg('grade'))['grade__avg']

        # subjects = Subject.objects.filter(id_subject__in=subject_ids)
        serializer = self.serializer_class(approved,many=True)
        data={}
        data['subjects'] =serializer.data
        data['average'] =average_grade
        return Response(data)
    


#5. Comprobar las materias que un estudiante ha reprobado.

class StudentFailedSubjectsList(generics.ListAPIView):

    """
    List all subjects that a specific student has failed.

    This endpoint retrieves a list of subjects for a given student where the student's grade is less than 3.
    It requires that the user is authenticated to access this endpoint.

    **Parameters:**
    - `student_id` (int): The ID of the student whose failed subjects are to be retrieved. This should be provided as a URL path parameter.

    **Response:**
    - Returns a list of subjects that the student has failed. Each subject includes details about the subject and the failing grade.
"""
    serializer_class = SubjectEstudentFailedSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        student_id = self.kwargs['student_id']  
        return Enrollment.objects.filter(student_id=student_id, grade__lt=3, grade__isnull=False)
    

#9. Un profesor finaliza la materia (califica cada estudiante)
class GradeUpdateView(generics.UpdateAPIView):

    """
    Update the grade for a specific student in a specific subject.

    This endpoint allows an authenticated user to update the grade for a student in a given subject.
    The grade is updated based on the provided `student_id` and `subject_id`.
    """
    serializer_class = GradeUpdateSerializer
    permission_classes = [IsAuthenticated]
    def update(self, request,id_student,id_subject):
        data = request.data
        instance = Enrollment.objects.filter(subject_id=id_subject,student=id_student).first()
        serializer = self.serializer_class(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


#10. Un profesor puede obtener las calificaciones de los estudiantes en sus materias

class SubjectEnrollmentGradeView(generics.ListAPIView):

    """
    List all students enrolled in a specific subject along with their grades.

    This endpoint retrieves a list of students who are enrolled in a specific subject and their corresponding grades. It requires that the user is authenticated to access this endpoint.

    **Parameters:**
    - `subject_id` (int): The ID of the subject for which the enrollment details are to be retrieved. This should be provided as a URL path parameter.

    **Response:**
    - Returns a list of students enrolled in the specified subject, including their grades.
    """
    serializer_class = EnrollmentGradeSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        subject_id = self.kwargs['subject_id']  
        return Enrollment.objects.filter(subject_id=subject_id)