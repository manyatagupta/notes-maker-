from django.db import models
from django.contrib.auth.models import User

class StudyMaterial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_materials')
    video_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255, default="YouTube Video Notes")
    notes = models.TextField()
    summary = models.TextField()
    quiz = models.JSONField()
    flashcards = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.video_id}"

    class Meta:
        ordering = ['-created_at']

