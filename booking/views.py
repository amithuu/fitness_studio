import logging
from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_class(request):
    """ Create a new fitness class with timezone management (IST) """
    name = request.data.get('name')
    date_time_str = request.data.get('date_time')  # Expecting format: 'YYYY-MM-DD HH:MM'
    instructor = request.data.get('instructor')
    available_slots = request.data.get('available_slots')

    try:
        # Convert string input to a timezone-aware datetime object in IST
        naive_datetime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
        aware_datetime = make_aware(naive_datetime)  # Converts it into the default timezone (IST)

        # Validation: Prevent duplicate class scheduling
        existing_class = FitnessClass.objects.filter(name=name, date_time=aware_datetime, instructor=instructor).exists()
        
        if existing_class:
            return Response({"error": "Class already exists on this date-time with the same instructor."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Save class with timezone-aware datetime
        fitness_class = FitnessClass.objects.create(
            name=name,
            date_time=aware_datetime,
            instructor=instructor,
            available_slots=available_slots
        )
        return Response(FitnessClassSerializer(fitness_class).data, status=status.HTTP_201_CREATED)

    except ValueError:
        return Response({"error": "Invalid date-time format. Use YYYY-MM-DD HH:MM."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_classes(request):
    classes = FitnessClass.objects.all()
    serializer = FitnessClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_class(request):
    """ Book a class with validation & error handling """
    class_id = request.data.get('class_id')
    client_name = request.data.get('client_name')
    client_email = request.data.get('client_email')

    # Ensure required fields exist
    if not class_id or not client_name or not client_email:
        return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = BookingSerializer(data=request.data)

    if not serializer.is_valid():  # Check if input is valid before proceeding
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        fitness_class = FitnessClass.objects.get(id=class_id)

        if fitness_class.available_slots > 0:
            booking = Booking.objects.create(
                class_booked=fitness_class,
                client_name=client_name,
                client_email=client_email
            )
            fitness_class.available_slots -= 1
            fitness_class.save()
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": f"No available slots for {(fitness_class.name).upper()} class, please check for other classes "}, status=status.HTTP_400_BAD_REQUEST)

    except FitnessClass.DoesNotExist:
        return Response({"error": f"Class not found.{fitness_class.name}"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Unexpected error while booking: {str(e)}")
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_bookings(request, email):
    bookings = Booking.objects.filter(client_email=email)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
