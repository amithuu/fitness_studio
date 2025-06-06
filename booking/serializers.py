from rest_framework import serializers
from django.utils.timezone import localtime
from .models import FitnessClass, Booking
import re
class FitnessClassSerializer(serializers.ModelSerializer):
    local_date_time = serializers.SerializerMethodField()

    def get_local_date_time(self, obj):
        return localtime(obj.date_time).strftime("%Y-%m-%d %H:%M")

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'local_date_time', 'instructor', 'available_slots']
        
    def validate_available_slots(self, value):
        """ Ensure available slots are a positive number """
        if value < 1:
            raise serializers.ValidationError("Available slots must be at least 1.")
        return value

    def validate_name(self, value):
        """ Prevent empty names or too short names """
        if len(value) < 3:
            raise serializers.ValidationError("Class name must be at least 3 characters.")
        return value

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
    class_booked = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), required=False)
    
    def validate_client_email(self, value):
            """ Ensure email format is correct """
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):  # Improved regex validation
                raise serializers.ValidationError("Invalid email format. Please enter a valid email.")
            return value
