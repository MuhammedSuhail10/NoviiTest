from rest_framework import serializers
from .models import *

class TaskSerial(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ReportSerial(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'worked_hours', 'completion_report']