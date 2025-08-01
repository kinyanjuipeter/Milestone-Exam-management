from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class CampusAccessMiddleware:
    """
    Middleware to ensure proper campus access control
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # List of URLs that don't require campus selection
        exempt_urls = [
            '/',  # Campus selection page
            '/admin/',
            '/admin/login/',
            '/manage-campus-passwords/',
        ]
        
        # Check if the current URL is exempt
        current_path = request.path
        is_exempt = any(current_path.startswith(url) for url in exempt_urls)
        
        # If user is not a superuser and trying to access campus password management
        if current_path == '/manage-campus-passwords/' and not request.user.is_superuser:
            messages.error(request, 'Access denied. Only administrators can manage campus passwords.')
            return redirect('exams:home')
        
        # For non-exempt URLs, check if user has selected a campus
        if not is_exempt and not request.user.is_superuser:
            campus_id = request.session.get('campus_id')
            if not campus_id:
                messages.warning(request, 'Please select a campus first.')
                return redirect('exams:campus_select')
        
        response = self.get_response(request)
        return response 