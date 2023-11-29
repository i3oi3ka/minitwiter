from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')
    email = models.CharField(max_length=128, unique=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.user.pk})

    def save(self, *args, **kwargs):
        if self.birthday:
            today = date.today()
            age = today.year - self.birthday.year - (
                    (today.month, today.day) < (self.birthday.month, self.birthday.day))
            self.age = age
        super(User, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars', default='users/avatars/default_avatar.jpg')

    def __str__(self):
        return f"'{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.user.pk})
