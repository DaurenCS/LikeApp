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
    likes = models.ManyToManyField('self', symmetrical=False, related_name='liked_by')

    def __str__(self):
        return self.user.username

