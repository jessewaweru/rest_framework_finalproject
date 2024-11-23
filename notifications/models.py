from django.db import models
from users.models import User
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}:{self.message[:20]}"
