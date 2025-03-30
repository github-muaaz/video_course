from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Video(models.Model):
    title = models.TextField(max_length=255)
    tutor = models.TextField(max_length=255)
    rate = models.FloatField()
    date_created = models.DateField(auto_now_add=True)
    image = models.FileField(upload_to='images/')
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Subscribed' if self.is_subscribed else 'Not Subscribed'}"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)

    class Meta:
        unique_together = ("user", "card_number")

    def __str__(self):
        return f"{self.user.username} - Card Ending in {self.card_number[-4:]}"
