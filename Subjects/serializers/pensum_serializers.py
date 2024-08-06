from rest_framework import serializers
from Subjects.models import Pensum
from .subject_serializers import SubjectSerializer


class PensumSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    
    class Meta:
        model = Pensum
        fields = '__all__'