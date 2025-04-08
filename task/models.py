from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending','pending'), ('progress','progress'), ('completed','completed')])
    completion_report = models.TextField(null=True, blank=True)
    worked_hours = models.IntegerField(null=True, blank=True)