from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer



@api_view(['POST'])
def create_class(request):
    name = request.data.get('name')
    date_time = request.data.get('date_time')
    instructor = request.data.get('instructor')
    available_slots = request.data.get('available_slots')

    # Validation: Check if the same instructor already scheduled the same class
    if FitnessClass.objects.filter(name=name, date_time=date_time, instructor=instructor).exists():
        return Response({"error": "This class already exists with the same instructor at this time."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Create and save the new class
    fitness_class = FitnessClass.objects.create(
        name=name,
        date_time=date_time,
        instructor=instructor,
        available_slots=available_slots
    )

    return Response(FitnessClassSerializer(fitness_class).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_classes(request):
    classes = FitnessClass.objects.all()
    serializer = FitnessClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_class(request):
    class_id = request.data.get('class_id')
    try:
        fitness_class = FitnessClass.objects.get(id=class_id)
        if fitness_class.available_slots > 0:
            booking = Booking.objects.create(
                class_booked=fitness_class,
                client_name=request.data.get('client_name'),
                client_email=request.data.get('client_email')
            )
            fitness_class.available_slots -= 1
            fitness_class.save()
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "No available slots"}, status=status.HTTP_400_BAD_REQUEST)
    except FitnessClass.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_bookings(request, email):
    bookings = Booking.objects.filter(client_email=email)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
