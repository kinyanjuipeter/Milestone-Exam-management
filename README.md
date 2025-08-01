# School Examination Management System

A comprehensive Django-based web application for managing student examination records and academic performance.

## 🎯 Features

### Core Functionality
- **Student Management**: Add and manage student information (name, registration number, course)
- **Course & Unit Management**: Organize academic structure with courses and units
- **Exam Record Entry**: Enter CAT 1, CAT 2, and End-term exam scores
- **Automatic Calculations**: Real-time calculation of CAT average and total average
- **Grade Assignment**: Automatic grade assignment based on total scores

### Advanced Features
- **Real-time Updates**: Live calculation of averages as you enter scores
- **Data Validation**: Ensures scores are within valid ranges (CAT: 0-30, End-term: 0-70)
- **Search & Filter**: Advanced filtering by course, unit, or student
- **Sortable Records**: Sort records by various criteria
- **Pagination**: Efficient handling of large datasets
- **Responsive Design**: Modern, mobile-friendly interface using Bootstrap 5

## 🏗️ Model Structure

### Database Models
- **Course**: Academic courses/programs
- **Unit**: Subjects within courses
- **Student**: Student information with unique registration numbers
- **ExamRecord**: Individual exam records linking students to units

### Key Relationships
- Units belong to Courses
- Students belong to Courses
- ExamRecords link Students to Units

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd exam-management-system

# Or download and extract the project files
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

### Step 7: Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000/`

## 📋 Usage Guide

### 1. Initial Setup
1. **Add Courses**: Go to "Manage" → "Courses" to add academic programs
2. **Add Units**: Go to "Manage" → "Units" to add subjects for each course
3. **Add Students**: Go to "Manage" → "Students" to register students

### 2. Entering Exam Marks
1. Navigate to "Enter Marks"
2. Select a student and unit
3. Enter CAT 1, CAT 2, and End-term scores
4. View real-time calculations of averages
5. Save the record

### 3. Viewing Records
1. Go to "View Records" to see all exam data
2. Use filters to search by course, unit, or student
3. Sort records by different criteria
4. Edit or delete records as needed

## 🎨 User Interface

### Navigation
- **Home**: Dashboard with statistics and quick actions
- **Enter Marks**: Form for adding exam records
- **View Records**: Table view with filtering and sorting
- **Manage**: Dropdown for managing courses, units, and students

### Design Features
- **Bootstrap 5**: Modern, responsive design
- **Font Awesome**: Professional icons throughout
- **Color-coded Grades**: Visual indicators for performance levels
- **Real-time Feedback**: Instant calculation updates

## 🔧 Technical Details

### Technology Stack
- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (default), PostgreSQL (production-ready)
- **Icons**: Font Awesome 6.0

### Key Components
- **Models**: Django ORM with proper relationships and validations
- **Views**: Function-based views with proper error handling
- **Forms**: Django forms with custom validation
- **Templates**: Reusable template structure with inheritance
- **Admin**: Django admin interface for data management

### Security Features
- CSRF protection on all forms
- Input validation and sanitization
- SQL injection prevention through ORM
- XSS protection through template escaping

## 📊 Grade System

### Score Ranges
- **CAT 1 & CAT 2**: 0-30 points each
- **End-term**: 0-70 points
- **CAT Average**: (CAT 1 + CAT 2) / 2
- **Total Average**: CAT Average + End-term

### Grade Assignment
- **A**: 80-100 points
- **B**: 70-79 points
- **C**: 60-69 points
- **D**: 50-59 points
- **F**: 0-49 points

## 🛠️ Customization

### Adding New Features
1. **New Models**: Add to `exams/models.py`
2. **New Views**: Add to `exams/views.py`
3. **New Templates**: Create in `templates/exams/`
4. **URL Configuration**: Update `exams/urls.py`

### Styling Changes
- Modify `templates/base.html` for global styles
- Add custom CSS in template blocks
- Update Bootstrap classes for layout changes

## 🚀 Deployment

### Production Setup
1. **Database**: Configure PostgreSQL in settings
2. **Static Files**: Run `python manage.py collectstatic`
3. **Environment Variables**: Set DEBUG=False and SECRET_KEY
4. **Web Server**: Configure with Gunicorn or uWSGI
5. **Reverse Proxy**: Set up Nginx or Apache

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
  - Student, course, and unit management
  - Exam record entry and viewing
  - Real-time calculations
  - Responsive design

---

**Built with ❤️ using Django and Bootstrap** 