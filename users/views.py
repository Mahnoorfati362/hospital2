from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

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
