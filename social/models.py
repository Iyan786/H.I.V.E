from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class UserProfile(AbstractUser):
    name = models.CharField(max_length=55, null=True, blank=True)
    lname = models.CharField(max_length=55, null=True, blank=True)
    desc = models.CharField(max_length=55, null=True, blank=True)
    country = models.CharField(max_length=55, null=True, blank=True, default="Country")
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    
    ACCOUNT_TYPE_CHOICES = [
        ("Public", "Public"),
        ("Private", "Private"),
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default="Public")

    profile = models.ImageField(null=True, blank=True, default='default.png')

    # Override default related_name to avoid conflicts
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="userprofile_groups",  # Change related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="userprofile_permissions",  # Change related_name
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.email}"

class Post(models.Model):
    MEDIA_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('music', 'Music'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True, null=True)
    media_type = models.CharField(choices=MEDIA_CHOICES, max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to='posts/images/', blank=True, null=True,  default='images.jpg')
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    music = models.FileField(upload_to='posts/music/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)  
    like = models.PositiveIntegerField(default=0)  
    dislike = models.PositiveIntegerField(default=0)  
    liked_by = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True)
    disliked_by = models.ManyToManyField(UserProfile, related_name='disliked_posts', blank=True)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    def __str__(self):
        return f"Post by {self.user.username} - {self.media_type}"

class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logos/', default='default_logo.jpg')
    title = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Site Settings"

class ChatMessage(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    photo = models.FileField(upload_to="chat_uploads/", blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.message[:30]}"