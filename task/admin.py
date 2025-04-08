from django.contrib import admin
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'completion_report', 'status', 'worked_hours')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        elif request.user.is_staff:
            return qs.filter(created_by=request.user)
        return qs.none()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_staff and obj and obj.created_by == request.user:
            return True
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(role="user")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Task, TaskAdmin)