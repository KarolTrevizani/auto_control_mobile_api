import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser

from django.utils import timezone
    

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser. Adds additional fields including name, email, 
    cnh, and type. Configures the email field as unique for authentication purposes.
    """

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    cnh = models.CharField(max_length=30, unique=True, null=True)
    type = models.CharField(max_length=20, default="General")
    
    REQUIRED_FIELDS = []
    
    
class PasswordResetToken(models.Model):
    """
    Model to manage password reset tokens for users. Includes a foreign key to the User model, a unique 
    UUID token, creation timestamp, and a usage flag. Provides a method to check if the token is expired 
    within 48 hours.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > (self.created_at + timezone.timedelta(hours=48))
