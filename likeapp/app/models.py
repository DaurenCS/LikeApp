from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # age = models.IntegerField()
    # faculty = models.CharField(max_length=150)
    # course = models.IntegerField()
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True)

    def __str__(self):
        return self.user.username


class ViewedProfiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='viewed_profiles')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='viewed_by')
    viewed_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_from")
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target_user")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_from', 'user_to')

class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
        
