from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Task
from .serializers import TaskSerial, ReportSerial
import datetime

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    user = request.user
    today = datetime.date.today()
    serializer = TaskSerial(Task.objects.filter(assigned_to=user, due_date__lte=today), many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def edit_tasks(request, id):
    data = request.data
    task = Task.objects.get(id=id)
    if 'status' not in data:
        return Response({"message": "Status is mandatory to update a task"})
    if data['status'] == "completed":
        if 'completion_report' and 'worked_hours' not in data:
            return Response({"message": "Completion report and working hours is mandatory to complete a task"})

        task.status = data['status']
        task.completion_report = data['completion_report']
        task.worked_hours = data['worked_hours']
    else:
        task.status = data['status']
    task.save()
    return Response({"message": "Task updated succesfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report(request, id):
    user = request.user
    if user.role in ["superuser", "admin"]:
        serializer = ReportSerial(Task.objects.get(status="completed", id=id))
        return Response(serializer.data)
    return Response({"message": "Unauthorized"})