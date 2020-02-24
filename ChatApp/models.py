from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CurrentChat(models.Model):
    user = models.CharField(max_length=20 , unique=False)
    for_user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.user

class Chat(models.Model):
    sender = models.CharField(max_length=20)
    message = models.TextField()
    reciever = models.CharField(max_length=20)
    date_time = models.DateTimeField(default = timezone.now())

    def __str__(self):
        return self.reciever
 