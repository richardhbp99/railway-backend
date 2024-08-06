from Subjects.models import Subject
from Teachers.models import Teacher
from rest_framework import serializers

from Students.models import Student
from Security.models import Person

class PersonStudentAproSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'

class StudentSubjectSerializer(serializers.ModelSerializer):
    person = PersonStudentAproSerializer()
    class Meta:
        model = Student
        fields = '__all__'