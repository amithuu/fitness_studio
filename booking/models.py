from django.db import models
from django.utils.timezone import make_aware, localtime, is_naive

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    available_slots = models.IntegerField()

    def __str__(self):
        return self.name

    def get_ist_time(self):
        """ Ensure stored datetime converts to IST before returning """
        return localtime(self.date_time)

    def save(self, *args, **kwargs):
        """ Convert naive datetime to IST before saving """
        if self.date_time and is_naive(self.date_time):  
            self.date_time = make_aware(self.date_time)  # Convert only if naive
        super().save(*args, **kwargs)
        
class Booking(models.Model):
    class_booked = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.client_name} - {self.class_booked.name}"
