# models.py

from django.db import models

class SpamEmail(models.Model):
    message_id = models.CharField(max_length=255)
    sender = models.EmailField()
    subject = models.TextField()
    body = models.TextField()
    detected_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.sender}"
