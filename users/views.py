from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils.timezone import now, timedelta
from .models import TemporaryRole

def assign_temporary_role(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to assign temporary roles.")
        return redirect("dashboard")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role_id = request.POST.get("role_id")
        duration_hours = int(request.POST.get("duration", 1))  # Default: 1 hour
        
        user = User.objects.get(id=user_id)
        role = Group.objects.get(id=role_id)
        duration = timedelta(hours=duration_hours)

        temp_role = TemporaryRole.objects.create(
            user=user,
            role=role,
            assigned_by=request.user,
            duration=duration,
            expires_at=now() + duration
        )
        user.groups.add(role)  # Role assign kar do
        
        messages.success(request, f"{user.username} assigned {role.name} for {duration_hours} hours!")
        return redirect("dashboard")

    users = User.objects.exclude(is_superuser=True)
    roles = Group.objects.all()
    return render(request, "users/assign_temporary_role.html", {"users": users, "roles": roles})


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')  # Dashboard template render karega


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            # User role ke mutabiq redirect karna
            if user.is_superuser:
                return redirect("admin_dashboard")  # Admin ka dashboard
            elif user.groups.filter(name="Doctor").exists():
                return redirect("doctor_dashboard")
            elif user.groups.filter(name="Guardian").exists():
                return redirect("guardian_dashboard")
            elif user.groups.filter(name="Patient").exists():
                return redirect("patient_dashboard")
            else:
                return redirect("home")  # Default Redirect

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Password hash karna
            user.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")  # Login page pe redirect
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, "users/signup.html", {"form": form})

# Create your views here.
