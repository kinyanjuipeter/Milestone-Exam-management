# Campus Password Management Security Features

## Overview
The campus password management system is designed with multiple layers of security to ensure that only authorized administrators can manage campus passwords. **All campuses now require passwords - users cannot access any campus without a password set by the administrator.**

## Security Layers

### 1. View-Level Security
- **Decorators**: The `manage_campus_passwords` view uses `@login_required` and `@user_passes_test(is_superuser)` decorators
- **Double-Check**: Additional check within the view to ensure only superusers can access
- **Access Denied**: Non-superusers are redirected with an error message
- **Password Required**: All campuses must have passwords set - no campus can be accessed without a password

### 2. Admin Interface Security
- **CampusPassword Admin**: Only superusers can view, add, edit, or delete campus passwords
- **Permission Methods**: All CRUD operations are restricted to superusers only
- **Empty Queryset**: Non-superusers see an empty list of campus passwords
- **Required Passwords**: Admin interface enforces that passwords cannot be empty

### 3. Middleware Security
- **CampusAccessMiddleware**: Automatically checks user permissions for campus password management
- **URL Protection**: Blocks access to `/manage-campus-passwords/` for non-superusers
- **Automatic Redirect**: Redirects unauthorized users with error messages

### 4. Template Security
- **Conditional Display**: Campus password management link only shows for superusers
- **Admin Link**: Direct link to Django admin for superusers only
- **Required Fields**: Password fields are marked as required in forms

## Access Control

### For Superusers (Administrators):
- ✅ Can access `/admin/` interface
- ✅ Can manage campus passwords via web interface
- ✅ Can view all campus data
- ✅ Can set/update campus passwords
- ✅ Can access all system features
- ✅ Must set passwords for all campuses

### For Regular Users:
- ❌ Cannot access campus password management
- ❌ Cannot view campus passwords in admin
- ❌ Cannot modify campus passwords
- ✅ Can only access their selected campus data
- ✅ **Must enter campus password (required for all campuses)**
- ❌ Cannot access any campus without a password

## Default Campus Passwords
The system has been configured with default passwords for all campuses:

- **THIKA CAMPUS**: `thika123`
- **NAIROBI CAMPUS**: `nairobi123`
- **NAKURU CAMPUS**: `nakuru123`
- **MOMBASA CAMPUS**: `mombasa123`
- **ELDORET CAMPUS**: `eldoret123`

**⚠️ IMPORTANT**: These are default passwords. Administrators should change these immediately after first login.

## How to Use

### Setting Campus Passwords (Admin Only):
1. Login to the system as a superuser
2. Go to `/admin/` or click "Admin" in the navbar
3. Navigate to "Campus passwords" section
4. Set passwords for each campus (required)
5. **Cannot leave passwords empty** - all campuses require passwords

### Regular User Access:
1. Visit the landing page
2. Select a campus
3. **Enter the campus password (required)**
4. Access campus-specific data

## Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

## Security Best Practices
1. Change the default admin password immediately
2. Change default campus passwords immediately
3. Use strong passwords for each campus
4. Regularly review campus password settings
5. Monitor access logs for suspicious activity
6. Only grant superuser privileges to trusted administrators
7. **Never leave campus passwords empty**

## Technical Implementation
- **Models**: `CampusPassword` model with secure password storage
- **Views**: Decorated with proper authentication checks
- **Admin**: Custom admin interface with permission restrictions
- **Middleware**: Automatic access control and redirection
- **Templates**: Conditional display based on user permissions
- **Validation**: Server-side validation ensures passwords are required
- **Migration**: Default passwords set via migration

## Error Messages
- "Access denied. [Campus Name] requires a password set by administrator."
- "Invalid password for this campus."
- "Password is required for [Campus Name]. Cannot leave empty."
- "Access denied. Only administrators can manage campus passwords." 