from django.test import TestCase
from django.utils.timezone import now
from rest_framework.test import APIClient
from .models import FitnessClass, Booking

class FitnessAPITests(TestCase):
    def setUp(self):
        """ Set up test data before each test runs """
        self.client = APIClient()

        # Create a sample fitness class
        self.class_data = {
            "name": "Cricket",
            "date_time": now(),
            "instructor": "Alice",
            "available_slots": 5
        }
        self.fitness_class = FitnessClass.objects.create(**self.class_data)

    def test_get_classes(self):
        """ Test fetching fitness classes """
        response = self.client.get('/api/classes/')
        self.assertEqual(response.status_code, 200)  # Expect successful response
        self.assertGreater(len(response.data), 0)  # Ensure classes exist

    def test_create_class(self):
        """ Test creating a fitness class with valid data """
        new_class = {
            "name": "Zumba",
            "date_time": "2025-06-15 10:00",
            "instructor": "Bob",
            "available_slots": 10
        }
        response = self.client.post('/api/classes/create/', new_class, format='json')
        self.assertEqual(response.status_code, 201)  # Expect successful creation
        self.assertEqual(response.data["name"], "Zumba")  # Ensure class is stored

    def test_duplicate_class_error(self):
        """ Ensure duplicate class creation is prevented """
        duplicate_class = {
            "name": "Cricket",
            "date_time": now(),
            "instructor": "Alice",
            "available_slots": 5
        }
        response = self.client.post('/api/classes/create/', duplicate_class, format='json')
        self.assertEqual(response.status_code, 400)  # Expect duplicate class error
        self.assertIn("error", response.data)

    def test_booking_slot_availability(self):
        """ Test successful booking and dynamically check slot reduction """
        
        initial_slots = self.fitness_class.available_slots
        
        booking_data = {
            "class_id": self.fitness_class.id,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        
        response = self.client.post('/api/book/', booking_data, format='json')
        
        self.assertEqual(response.status_code, 201)
        
        # Refresh instance to get updated slots
        self.fitness_class.refresh_from_db()
        
        expected_slots = initial_slots - 1
        
        self.assertEqual(self.fitness_class.available_slots, expected_slots)


    def test_overbooking_error(self):
        """ Ensure booking fails when no slots remain """
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        booking_data = {
            "class_id": self.fitness_class.id,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        response = self.client.post('/api/book/', booking_data, format='json')
        self.assertEqual(response.status_code, 400)  # Expect failure
        self.assertIn("error", response.data)

    def test_get_bookings(self):
        """ Test retrieving bookings for a client """
        Booking.objects.create(class_booked=self.fitness_class, client_name="John Doe", client_email="john@example.com")

        response = self.client.get(f'/api/bookings/john@example.com/')
        self.assertEqual(response.status_code, 200)  # Expect success
        self.assertGreater(len(response.data), 0)  # Should return bookings

    def test_invalid_email_booking(self):
        """ Ensure incorrect email format is rejected """
        booking_data = {
            "class_id": self.fitness_class.id,
            "client_name": "John Doe",
            "client_email": "invalid-email"
        }

        response = self.client.post('/api/book/', booking_data, format='json')
        
        print("Response Data:", response.data)  # Debugging output
        
        self.assertEqual(response.status_code, 400)  # Expect failure
        self.assertIn("error", response.data)  # Ensure an error message is present


