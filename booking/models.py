from django.db import models

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    available_slots = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    class_booked = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.client_name} - {self.class_booked.name}"
