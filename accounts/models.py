from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Custom groups field to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',  # Unique related_name to avoid clashes
        blank=True
    )

    # Custom user_permissions field to avoid reverse accessor clashes
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_permissions',  # Unique related_name to avoid clashes
        blank=True
    )

    # Optionally, you can add other custom fields specific to your application:
    phone = models.CharField(max_length=15, blank=True, null=True)

    # The following line can be added if you're using email as the primary login
    # USERNAME_FIELD = 'email'  # Uncomment if you want to use email for authentication instead of the username
    # REQUIRED_FIELDS = ['email']  # Uncomment if you set USERNAME_FIELD to 'email'

    def __str__(self):
        return self.username

class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/', null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
    
class State(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to='images/', null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.name
    
class Footer(models.Model):
    tagline = models.TextField()
    copyright = models.TextField()
    logo = models.ImageField(upload_to='images/', null=False, blank=False)
    
    def __str__(self):
            return f"{self.tagline} - {self.copyright}"
