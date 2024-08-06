from Students.models import Student
from Security.models import Person

from rest_framework import serializers


class PersonStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    person = PersonStudentSerializer()
    class Meta:
        model = Student
        fields = '__all__'