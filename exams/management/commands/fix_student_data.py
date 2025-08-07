from django.core.management.base import BaseCommand
from exams.models import Student


class Command(BaseCommand):
    help = 'Fix student registration numbers that contain names instead of proper admission numbers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find students with problematic registration numbers
        problematic_students = []
        
        for student in Student.objects.all():
            reg_num = student.registration_number.strip()
            
            # Check if registration number looks like a name (contains only letters and spaces)
            if reg_num and reg_num.replace(' ', '').isalpha() and len(reg_num) > 3:
                problematic_students.append(student)
        
        if not problematic_students:
            self.stdout.write(
                self.style.SUCCESS('No students with problematic registration numbers found.')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'Found {len(problematic_students)} students with problematic registration numbers:')
        )
        
        for student in problematic_students:
            self.stdout.write(f'  - {student.name}: "{student.registration_number}"')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('\nThis was a dry run. No changes were made.')
            )
            self.stdout.write(
                'To fix these issues, run the command without --dry-run and manually update each student.'
            )
            return
        
        self.stdout.write(
            self.style.WARNING('\nPlease manually fix these registration numbers through the Django admin:')
        )
        self.stdout.write('1. Go to http://127.0.0.1:8000/admin/')
        self.stdout.write('2. Navigate to Students')
        self.stdout.write('3. Edit each student and update their registration number')
        self.stdout.write('4. Use a proper format like "MIN/01/102/23" or similar')
        
        # Show specific instructions for each student
        for i, student in enumerate(problematic_students, 1):
            self.stdout.write(f'\n{i}. Student: {student.name}')
            self.stdout.write(f'   Current registration number: "{student.registration_number}"')
            self.stdout.write(f'   Suggested format: "MIN/01/{100+i:03d}/23" (or your preferred format)') 