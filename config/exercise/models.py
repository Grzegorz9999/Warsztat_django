from django.db import models

class Room(models.Model):
    name = models.TextField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)

class RoomReservation(models.Model):
    room_id = models.ForeignKey('Room', on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(max_length=1000, blank=True)

class Meta:
    unique_together = ('room_id','date')

# Create your models here.
