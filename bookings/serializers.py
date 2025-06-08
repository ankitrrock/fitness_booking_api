from rest_framework import serializers
from .models import FitnessClass, Booking

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'date_time', 'instructor', 'available_slots']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booking_time']
