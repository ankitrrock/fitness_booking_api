from django.urls import path
from .views import FitnessClassListView, BookClassView, BookingListView

urlpatterns = [
    path('classes/', FitnessClassListView.as_view(), name='fitness-classes'),
    path('book/', BookClassView.as_view(), name='book-class'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
]
