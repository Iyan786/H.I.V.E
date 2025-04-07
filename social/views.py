from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from social.models import *
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from django.http import JsonResponse
from datetime import timedelta
import os
import subprocess
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def reg(request):
    settings = SiteSettings.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('username')
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same.")
        else:
            try:
                # Use the custom create_user method in UserProfileManager
                my_user = UserProfile.objects.create_user(name=name, username=uname, gender=gender, email=email, password=pass1)
                my_user.save()
                return redirect('index')  # Redirect to the home page after successful signup
            except Exception as e:
                return HttpResponse(f"Error: {str(e)}")
    return render(request,"reg.html",{'settings': settings})

def loginpage(request):
    settings = SiteSettings.objects.first()
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)

        if user and user.is_superuser:
            login(request,user)
            return redirect('/dashboard')
        
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse("Username or password is incorrect!!!")
    return render(request,"loginpage.html", {'settings': settings})

def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('loginpage')  


@login_required
def editprofile(request):
    Site = SiteSettings.objects.first() 
    users = UserProfile.objects.all()
    user = request.user  # Get the logged-in user

    if request.method == "POST":
        if "profile_image" in request.FILES:
            profile = request.FILES["profile_image"]
            user.profile = profile
            user.save()
        else:
            # Collecting data from the POST request
            name = request.POST.get('name', user.name)
            username = request.POST.get('username', user.username)
            email = request.POST.get('email', user.email)
            gender = request.POST.get('gender', user.gender)
            desc = request.POST.get('desc', user.desc)
            country = request.POST.get('country', user.country)
            account_type = request.POST.get('account_type', user.account_type)  # New field

            day = request.POST.get("dob_day")
            month = request.POST.get("dob_month")
            year = request.POST.get("dob_year")

            # Updating user fields
            user.name = name
            user.username = username
            user.email = email
            user.gender = gender
            user.desc = desc
            user.country = country
            user.account_type = account_type  # Save the account type

            # Validate and update DOB
            try:
                dob = datetime.date(int(year), int(month), int(day))  # Convert to YYYY-MM-DD
                user.dob = dob
            except ValueError:
                messages.error(request, "Invalid date. Please enter a valid date.")
                return redirect('editprofile')

            # Save the updated profile
            user.save()
            messages.success(request, "Profile updated successfully.")
            
        return redirect('editprofile')

    return render(request, "edit-profile-basic.html", {'user': user, 'Site': Site})

def users(request):
    settings = SiteSettings.objects.first()
    users = UserProfile.objects.filter(is_superuser=False)
    return render(request,"dashboard/user.html", {'users': users,'settings': settings})

@login_required
def add_post(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    Site = SiteSettings.objects.first()
    users = UserProfile.objects.all()
    user = request.user

    if request.method == 'POST':
        caption = request.POST.get('caption')
        photo = request.FILES.get('image')
        video = request.FILES.get('video')
        music = request.FILES.get('music')

        # Determine media type based on uploaded file
        media_type = None

        # Image Compression
        if photo:
            media_type = 'image'
            image = Image.open(photo)
            image = image.convert("RGB")  # Convert to RGB (for consistency)
            
            output = BytesIO()
            image.save(output, format='JPEG', quality=70)  # Reduce quality to 70%
            output.seek(0)

            # Create a compressed in-memory image file
            photo = InMemoryUploadedFile(
                output, 'ImageField', photo.name, 'image/jpeg', output.getbuffer().nbytes, None
            )

        # Video Compression using FFmpeg
        elif video:
            media_type = 'video'
            video_name = f"compressed_{video.name}"
            input_video_path = os.path.join(settings.MEDIA_ROOT, "posts/videos/", video.name)
            output_video_path = os.path.join(settings.MEDIA_ROOT, "posts/videos/", video_name)

            # Save original video temporarily
            with open(input_video_path, 'wb+') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)

            # Compress video using FFmpeg
            subprocess.run([
                "ffmpeg", "-i", input_video_path, "-vcodec", "libx264", "-crf", "28", output_video_path
            ])

            # Replace uploaded video with compressed version
            video = f"posts/videos/{video_name}"

        elif music:
            media_type = 'music'

        # Save the post
        post = Post.objects.create(
            user=request.user,
            caption=caption,
            media_type=media_type,
            photo=photo,
            video=video,
            music=music
        )
        post.save()
        return redirect('index')  # Redirect after successful post creation

    return render(request, 'index.html', {'posts': posts, 'Site': Site, 'users': users, 'user': user})

def delete_user(request, id):
    user = get_object_or_404(UserProfile, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('/users')
    return render(request, 'dashboard/product_confirm_delete.html',{'user': user})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)  # Ensure user owns the post
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('index')

def dashboard(request):
    settings, created = SiteSettings.objects.get_or_create(id=1)  # Ensures at least one instance
    user_count = UserProfile.objects.count()
    new_users = UserProfile.objects.filter(date_joined__gte=now() - timedelta(days=30)).count()

    if request.method == 'POST':
        logo = request.FILES.get('logo')
        title = request.POST.get('logoTitle', '')  # Get the optional title

        if logo:
            settings.logo = logo
        if title:
            settings.title = title   # Assuming there's a field in your model
            settings.save()
            messages.success(request, "Logo updated successfully!")  # Flash message
        else:
            messages.error(request, "Please select a logo before uploading.")

        return redirect('dashboard')

    return render(request, 'dashboard.html', {'settings': settings, 'user_count': user_count, 'new_users': new_users})

@login_required
def edit_pass(request):
    Site = SiteSettings.objects.first()
    user = request.user 
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

         # Get the logged-in user

        # Check if current password is correct
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('edit_password')

        # Check if new passwords match
        if new_password != confirm_new_password:
            messages.error(request, "New passwords do not match.")
            return redirect('edit_password')

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully.")
        return redirect('index')  # Redirect to profile or dashboard

    return render(request, 'edit-password.html', {'Site': Site})

def profile(request):
    Site = SiteSettings.objects.first()
    user = request.user 
    return render(request, 'about.html', {'Site': Site})

def feed(request):
    Site = SiteSettings.objects.first()
    liked_posts = request.user.liked_posts.values_list('id', flat=True)
    user = request.user 
    posts = Post.objects.filter(user__account_type="Public").order_by('?')
    users = UserProfile.objects.all()
    return render(request, 'time-line.html', {'Site': Site,'users': users,'posts': posts, 'liked_posts': liked_posts})

@csrf_exempt
def increment_views(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            post.increment_views()
            return JsonResponse({'success': True, 'views': post.views})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            user = request.user

            if not user.is_authenticated:
                return JsonResponse({'success': False, 'error': 'User not authenticated.'}, status=401)

            if user in post.liked_by.all():
                return JsonResponse({'success': False, 'error': 'You have already liked this post.'}, status=400)

            if user in post.disliked_by.all():
                post.disliked_by.remove(user)

            post.liked_by.add(user)

            # Update both counts
            post.like = post.liked_by.count()
            post.dislike = post.disliked_by.count()
            post.save(update_fields=['like', 'dislike'])

            return JsonResponse({
                'success': True,
                'likes': post.like,
                'dislikes': post.dislike  # ✅ include this
            })
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


@login_required
def dislike_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            user = request.user

            if user in post.disliked_by.all():
                return JsonResponse({'success': False, 'error': 'You have already disliked this post.'}, status=400)

            if user in post.liked_by.all():
                post.liked_by.remove(user)

            post.disliked_by.add(user)

            # Update both counts
            post.like = post.liked_by.count()
            post.dislike = post.disliked_by.count()
            post.save(update_fields=['like', 'dislike'])

            return JsonResponse({
                'success': True,
                'likes': post.like,        # ✅ include this
                'dislikes': post.dislike
            })
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@login_required
def chat_view(request, receiver_username):
    Site = SiteSettings.objects.first()
    """ Fetch messages between the logged-in user and the receiver """
    messages1 = ChatMessage.objects.filter(
        sender=request.user, receiver__username=receiver_username
    ) | ChatMessage.objects.filter(
        sender__username=receiver_username, receiver=request.user
    ).order_by("timestamp")

    return render(request, 'chat.html', {"messages1": messages1, "receiver": receiver_username})

@login_required
def messages1(request, receiver_username):
    user = request.user
    receiver = get_object_or_404(UserProfile, username=receiver_username)

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        photo = request.FILES.get("photo")

        if message_text or photo:  # Ensure at least one of them is sent
            new_message = ChatMessage.objects.create(
                sender=user, receiver=receiver, message=message_text, photo=photo
            )

            return JsonResponse({
                "sender": user.username,
                "message": new_message.message or "",
                "photo_url": new_message.photo.url if new_message.photo else None
            })

    messages1 = ChatMessage.objects.filter(
        sender=user, receiver=receiver
    ) | ChatMessage.objects.filter(
        sender=receiver, receiver=user
    ).order_by("timestamp")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "messages1": [
                {"sender": msg.sender.username, "message": msg.message or "", 
                 "photo_url": msg.photo.url if msg.photo else None} 
                for msg in messages1
            ]
        })

    return render(request, "messages.html", {
        "messages1": messages1,
        "receiver_username": receiver_username,
        "receiver_profile": receiver.profile.url,
        "sender_profile": user.profile.url,
        "users": UserProfile.objects.all(),
        "Site": SiteSettings.objects.first(),
    })

def manage_post(request):
    users = UserProfile.objects.all()
    return render(request, "dashboard/manage_posts.html", {"users": users})

def user_detail_view(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id, is_superuser=False)  
    posts = Post.objects.filter(user=user)  # Fetch posts created by the user
    return render(request, "dashboard/user_detail.html", {"user": user, "posts": posts})

def ban_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_banned = True
    post.save()
    messages.success(request, "Post has been banned as inappropriate.")
    return redirect("user-detail", user_id=post.user.id)  # Redirect to user's detail page

def unban_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_banned = False
    post.save()
    messages.success(request, "Post has been unbanned.")
    return redirect("user-detail", user_id=post.user.id)

@login_required
def adelete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)  # Ensure user owns the post
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('user-detail', user_id=post.user.id)
