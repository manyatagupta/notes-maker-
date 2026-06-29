from django.db import models
from django.contrib.auth.models import User

import uuid
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    last_active_date = models.DateField(default=timezone.now)
    current_streak = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} Profile"

class StudyMaterial(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('youtube', 'YouTube Video'),
        ('article', 'Article'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_materials')
    video_id = models.CharField(max_length=50, blank=True, default='')
    source_url = models.URLField(max_length=500, blank=True, default='')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='youtube')
    title = models.CharField(max_length=255, default="YouTube Video Notes")
    notes = models.TextField()
    summary = models.TextField()
    quiz = models.JSONField()
    flashcards = models.JSONField(default=list)
    mindmap = models.TextField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    is_mastered = models.BooleanField(default=False)
    tags = models.CharField(max_length=255, blank=True, null=True)
    share_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        ordering = ['-created_at']
