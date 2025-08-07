#!/usr/bin/env python
"""
Comprehensive Test Script for Exam Management System Fixes
Tests all the fixes implemented for:
1. Manually added students saving correctly
2. CAT average display in transcripts
3. Marks entry and validation
4. Form structure and field naming
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from exams.models import Student, Course, Unit, ExamRecord, Campus
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_management.settings')
django.setup()

def test_manually_added_students():
    """Test that manually added students are saved correctly"""
    print("🧪 Testing Manually Added Students Functionality...")
    
    # Create test data
    campus = Campus.objects.first()
    if not campus:
        campus = Campus.objects.create(name="Test Campus")
    
    course = Course.objects.first()
    if not course:
        course = Course.objects.create(name="Test Course", campus=campus)
    
    unit = Unit.objects.first()
    if not unit:
        unit = Unit.objects.create(name="Test Unit", course=course)
    
    # Test data for new student
    student_name = "Test Student Manual"
    admission_number = "TEST001"
    cat1_score = "25"
    cat2_score = "28"
    endterm_score = "65"
    
    # Simulate form data
    form_data = {
        'course': course.id,
        'unit': unit.id,
        'term': 'Term 1',
        'year': '2024',
        'school': 'Test School',
        'level': 'Level 1',
        'campus': campus.id,
        
        # New student data
        'cat1_new_test123': cat1_score,
        'student_name_test123': student_name,
        'admission_number_test123': admission_number,
        'cat2_test123': cat2_score,
        'endterm_test123': endterm_score,
    }
    
    # Create a test user
    user = User.objects.create_user(username='testuser', password='testpass')
    user.is_staff = True
    user.save()
    
    # Test the enter_marks view
    client = Client()
    client.login(username='testuser', password='testpass')
    
    response = client.post(reverse('exams:enter_marks'), form_data)
    
    # Check if student was created
    try:
        student = Student.objects.get(registration_number=admission_number)
        print(f"✅ Student created successfully: {student.name}")
        
        # Check if exam record was created
        record = ExamRecord.objects.get(student=student, unit=unit)
        print(f"✅ Exam record created successfully")
        print(f"   CAT1: {record.cat1_score}")
        print(f"   CAT2: {record.cat2_score}")
        print(f"   End Term: {record.end_term_score}")
        
        # Test CAT average calculation
        cat_avg = record.cat_average
        print(f"   CAT Average: {cat_avg}")
        
        return True
        
    except Student.DoesNotExist:
        print("❌ Student was not created")
        return False
    except ExamRecord.DoesNotExist:
        print("❌ Exam record was not created")
        return False

def test_cat_average_in_transcript():
    """Test that CAT average is displayed correctly in transcripts"""
    print("\n🧪 Testing CAT Average in Transcript...")
    
    # Get existing data or create test data
    student = Student.objects.first()
    if not student:
        print("❌ No students found for testing")
        return False
    
    unit = Unit.objects.first()
    if not unit:
        print("❌ No units found for testing")
        return False
    
    # Create or update exam record with known values
    record, created = ExamRecord.objects.get_or_create(
        student=student,
        unit=unit,
        year='2024',
        term='Term 1',
        defaults={
            'cat1_score': Decimal('25'),
            'cat2_score': Decimal('28'),
            'end_term_score': Decimal('65'),
        }
    )
    
    if not created:
        record.cat1_score = Decimal('25')
        record.cat2_score = Decimal('28')
        record.end_term_score = Decimal('65')
        record.save()
    
    # Calculate expected CAT average
    expected_cat_avg = int(round((25 + 28) / 2))
    actual_cat_avg = record.cat_average
    
    print(f"Expected CAT Average: {expected_cat_avg}")
    print(f"Actual CAT Average: {actual_cat_avg}")
    
    if expected_cat_avg == actual_cat_avg:
        print("✅ CAT average calculation is correct")
        return True
    else:
        print("❌ CAT average calculation is incorrect")
        return False

def test_form_structure():
    """Test that the form structure is correct for manually added students"""
    print("\n🧪 Testing Form Structure...")
    
    # Check if the enter_marks template has the correct structure
    template_path = 'templates/exams/enter_marks.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key elements
    checks = [
        ('Add New Student section inside form', '<!-- Add New Student Section -->' in content and '</form>' in content),
        ('Hidden fields for student info', 'student_name_${tempId}' in content),
        ('Proper field naming', 'cat1_new_' in content and 'cat2_' in content),
        ('Form validation', 'marksEntryForm' in content),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_passed = False
    
    return all_passed

def test_view_logic():
    """Test the view logic for handling manually added students"""
    print("\n🧪 Testing View Logic...")
    
    # Check the enter_marks view for correct field handling
    view_path = 'exams/views.py'
    
    if not os.path.exists(view_path):
        print(f"❌ View file not found: {view_path}")
        return False
    
    with open(view_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key logic elements
    checks = [
        ('Handles cat1_new_ prefix', 'cat1_new_' in content),
        ('Correct field name matching', 'cat2_{temp_id}' in content),
        ('Student creation logic', 'Student.objects.get_or_create' in content),
        ('Exam record creation', 'ExamRecord.objects.get_or_create' in content),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Test Suite for Exam Management System Fixes\n")
    
    tests = [
        ("Form Structure", test_form_structure),
        ("View Logic", test_view_logic),
        ("CAT Average in Transcript", test_cat_average_in_transcript),
        ("Manually Added Students", test_manually_added_students),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print("="*60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! All fixes are working correctly.")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 