from django.db import models
from django.urls import reverse
from users.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    title = models.CharField(max_length=128, blank=True, null=False)
    text = models.TextField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('message_detail', kwargs={'pk': self.pk})


    def __str__(self):
        return f'{self.title} {self.text}'
