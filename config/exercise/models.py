from django.db import models

class Room(models.Model):
    name = models.TextField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)

# Create your models here.
