from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Course, Unit, Student, ExamRecord, Campus, CampusPassword


def is_superuser(user):
    return user.is_superuser


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    
    def get_queryset(self, request):
        # Superusers can see all campuses, regular users see only their campus
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(id=request.session.get('campus_id'))


@admin.register(CampusPassword)
class CampusPasswordAdmin(admin.ModelAdmin):
    list_display = ['campus', 'created_at', 'updated_at']
    search_fields = ['campus__name']
    ordering = ['campus__name']
    
    def get_queryset(self, request):
        # Only superusers can see campus passwords
        if request.user.is_superuser:
            return super().get_queryset(request)
        return self.model.objects.none()  # Return empty queryset for non-superusers
    
    def has_add_permission(self, request):
        # Only superusers can add campus passwords
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        # Only superusers can change campus passwords
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete campus passwords
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        # Only superusers can view campus passwords
        return request.user.is_superuser


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'campus', 'created_at', 'updated_at']
    list_filter = ['campus']
    search_fields = ['name']
    ordering = ['name']
    
    def get_queryset(self, request):
        # Superusers can see all courses, regular users see only their campus courses
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        campus_id = request.session.get('campus_id')
        if campus_id:
            return qs.filter(campus_id=campus_id)
        return qs.none()


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'campus', 'created_at', 'updated_at']
    list_filter = ['course', 'campus']
    search_fields = ['name', 'course__name']
    ordering = ['course', 'name']
    
    def get_queryset(self, request):
        # Superusers can see all units, regular users see only their campus units
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        campus_id = request.session.get('campus_id')
        if campus_id:
            return qs.filter(campus_id=campus_id)
        return qs.none()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'course', 'campus', 'created_at', 'updated_at']
    list_filter = ['course', 'campus']
    search_fields = ['name', 'registration_number', 'course__name']
    ordering = ['name']
    
    def get_queryset(self, request):
        # Superusers can see all students, regular users see only their campus students
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        campus_id = request.session.get('campus_id')
        if campus_id:
            return qs.filter(campus_id=campus_id)
        return qs.none()


@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'unit', 'cat1_score', 'cat2_score', 'cat_average', 'end_term_score', 'total_average', 'campus']
    list_filter = ['unit__course', 'unit', 'campus']
    search_fields = ['student__name', 'student__registration_number', 'unit__name']
    readonly_fields = ['cat_average', 'total_average']
    ordering = ['student__name', 'unit__name']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'unit')
        }),
        ('Exam Scores', {
            'fields': ('cat1_score', 'cat2_score', 'end_term_score')
        }),
        ('Calculated Averages', {
            'fields': ('cat_average', 'total_average'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        # Superusers can see all records, regular users see only their campus records
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        campus_id = request.session.get('campus_id')
        if campus_id:
            return qs.filter(campus_id=campus_id)
        return qs.none()


# Custom User Admin for superadmin functionality
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 