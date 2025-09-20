from django.shortcuts import redirect
from django.urls import reverse

class RestrictAdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If a non-staff user tries to access /admin/
        if request.path.startswith(reverse("admin:index")):
            if not request.user.is_staff:
                return redirect("dashboard")  # 🚀 send kids to dashboard
        return self.get_response(request)
