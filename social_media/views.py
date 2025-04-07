from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from social.models import *
from django.contrib import messages
from django.http import HttpResponse

def index(request):
    return render(request,"index.html")

# def landing(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         gender = request.POST.get("gender")
#         email = request.POST.get("email")

#         # Check if username or email already exists
#         if UserProfile.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#         elif UserProfile.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists.")
#         else:
#             # Create and save the new user
            # user = UserProfile(
            #     name=name,
            #     username=username,
            #     password=password,  # Consider hashing passwords in production
            #     gender=gender,
            #     email=email
            # )
#             user.save()
#             messages.success(request, "Registration successful!")
#             return redirect("index")

#     return render(request, "landing.html")

# def LoginPage(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username,password=pass1)

        if user and user.is_superuser:
            login(request,user)
            return redirect('index')
        
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
#             return HttpResponse("Username or password is incorrect!!!")
        
#     return render(request,'landing.html')

def login_register(request):
    if request.method == "POST":
        if "signin" in request.POST:  # Check if login form is submitted
            username = request.POST.get("username")
            password = request.POST.get("pass")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")  # Redirect after login
            else:
                messages.error(request, "Invalid username or password")

        elif "signup" in request.POST:  # Check if registration form is submitted
           name = request.POST.get("name")
           username = request.POST.get("username")
           password = request.POST.get("password")
           gender = request.POST.get("gender")
           email = request.POST.get("email")

#         # Check if username or email already exists
           if UserProfile.objects.filter(username=username).exists():
              messages.error(request, "Username already exists.")
           elif UserProfile.objects.filter(email=email).exists():
              messages.error(request, "Email already exists.")
           else:
              # Create and save the new user
              user = UserProfile(
                  name=name,
                  username=username,
                  password=password,  # Consider hashing passwords in production
                  gender=gender,
                  email=email
            )
               user.save()
               messages.success(request, "Registration successful!")
               return redirect("index")

    return render(request, "landing.html")
    