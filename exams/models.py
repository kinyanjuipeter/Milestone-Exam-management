from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Campus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class CampusPassword(models.Model):
    campus = models.OneToOneField(Campus, on_delete=models.CASCADE, related_name='password')
    password = models.CharField(max_length=128, help_text="Password for this campus")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Password for {self.campus.name}"


class School(models.Model):
    """Model for storing school information."""
    name = models.CharField(max_length=100)  # Removed unique=True
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='schools')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        # Add unique constraint for name + campus to prevent duplicates within the same campus
        unique_together = ['name', 'campus']


class Course(models.Model):
    """Model for storing course information."""
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        # Add unique constraint for name + school to prevent duplicates within the same school
        unique_together = ['name', 'school']


class Unit(models.Model):
    """Model for storing unit/subject information."""
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.course.name}"

    class Meta:
        unique_together = ['name', 'course']
        ordering = ['course', 'name']


class Student(models.Model):
    """Model for storing student information."""
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.registration_number})"

    class Meta:
        ordering = ['name']


class ExamRecord(models.Model):
    """Model for storing exam records for each student and unit."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_records')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='exam_records')
    cat1_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        help_text="CAT 1 score out of 30"
    )
    cat2_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        help_text="CAT 2 score out of 30"
    )
    end_term_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(70)],
        help_text="End-term exam score out of 70"
    )
    term = models.CharField(max_length=10, help_text="Term (e.g. I, II, III)", default="I")
    year = models.IntegerField(help_text="Year (e.g. 2025)", default=2025)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.unit.name}"

    @property
    def cat_average(self):
        """Calculate CAT average = (CAT 1 + CAT 2) / 2"""
        return (self.cat1_score + self.cat2_score) / 2

    @property
    def total_average(self):
        """Calculate total average = CAT Average + End Term"""
        return self.cat_average + self.end_term_score

    class Meta:
        unique_together = ['student', 'unit', 'term', 'year']
        ordering = ['student__name', 'unit__name']
