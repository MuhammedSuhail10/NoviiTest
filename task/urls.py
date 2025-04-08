from django.urls import path
from .views import *

urlpatterns = [
    path("", get_tasks),
    path("<int:id>", edit_tasks),
    path("<int:id>/report", get_report),
]