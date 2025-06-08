from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

import logging

logger = logging.getLogger(__name__)

# GET /classes/
class FitnessClassListView(generics.ListAPIView):
    queryset = FitnessClass.objects.upcoming()
    serializer_class = FitnessClassSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        logger.info(f"FitnessClassListView accessed by user {request.user}. Returned {len(response.data)} classes.")
        return response

# POST /book/
class BookClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        class_id = request.data.get('class_id')
        client_name = request.data.get('client_name')
        client_email = request.data.get('client_email')

        if not all([class_id, client_name, client_email]):
            logger.warning(f"Booking failed - Missing fields. User: {request.user}")
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                fitness_class = FitnessClass.objects.select_for_update().get(id=class_id)

                if fitness_class.available_slots <= 0:
                    logger.info(f"No slots left - class_id {class_id}, client_email {client_email}")
                    return Response({'error': 'No slots available for this class.'}, status=status.HTTP_400_BAD_REQUEST)

                # Optional: Prevent duplicate booking
                existing_booking = Booking.objects.filter(
                    fitness_class=fitness_class,
                    client_email=client_email
                ).first()
                if existing_booking:
                    logger.info(f"Duplicate booking attempt - class_id {class_id}, client_email {client_email}")
                    return Response({'error': 'You have already booked this class.'}, status=status.HTTP_400_BAD_REQUEST)

                # Create booking
                booking = Booking.objects.create(
                    fitness_class=fitness_class,
                    client_name=client_name,
                    client_email=client_email
                )

                # Reduce available slots
                fitness_class.available_slots -= 1
                fitness_class.save()

            logger.info(f"Booking successful - booking_id {booking.id}, class_id {class_id}, client_email {client_email}, user {request.user}")

            return Response(
                {
                    'message': 'Booking successful.',
                    'booking_id': booking.id
                },
                status=status.HTTP_201_CREATED
            )

        except FitnessClass.DoesNotExist:
            logger.error(f"Booking failed - class_id {class_id} not found. User: {request.user}")
            return Response({'error': 'Fitness class not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during booking. User: {request.user}")
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# GET /bookings/?email=
class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.request.query_params.get('email')
        queryset = Booking.objects.none()

        if email:
            queryset = Booking.objects.by_client_email(email)

        logger.info(f"BookingListView accessed by user {self.request.user}. Email filter: {email}. Returned {queryset.count()} bookings.")
        return queryset
