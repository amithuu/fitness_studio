from django.urls import path
from .views import get_classes, book_class, get_bookings, create_class

urlpatterns = [
    path('classes/', get_classes),
    path('classes/create/', create_class),  # Create new class
    path('book/', book_class),
    path('bookings/<str:email>/', get_bookings),
]
