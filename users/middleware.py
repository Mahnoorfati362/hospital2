# from django.shortcuts import redirect

# class RoleRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if request.path.startswith("/admin/") and request.user.role != "super_admin":
#                 return redirect("/")  # Unauthorized access blocked
#         return self.get_response(request)
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class RoleRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, "user") or not request.user.is_authenticated:
            return None  # Agar user attribute nahi mila ya user authenticated nahi hai toh proceed karein

        if request.path.startswith("/admin/") and request.user.role != "super_admin":
            return redirect("/")  # Unauthorized access blocked

