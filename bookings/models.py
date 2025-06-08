from django.db import models
from django.utils import timezone

# Custom QuerySet for FitnessClass
class FitnessClassQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(date_time__gte=timezone.now()).order_by('date_time')

    def available(self):
        return self.filter(available_slots__gt=0)

    def by_instructor(self, instructor_name):
        return self.filter(instructor__iexact=instructor_name)


# Manager for FitnessClass
class FitnessClassManager(models.Manager):
    def get_queryset(self):
        return FitnessClassQuerySet(self.model, using=self._db)

    def upcoming(self):
        return self.get_queryset().upcoming()

    def available(self):
        return self.get_queryset().available()

    def by_instructor(self, instructor_name):
        return self.get_queryset().by_instructor(instructor_name)


class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField(db_index=True)  # Add index here
    instructor = models.CharField(max_length=100)
    available_slots = models.PositiveIntegerField(default=10)

    objects = FitnessClassManager()

    class Meta:
        indexes = [
            models.Index(fields=['date_time']),
            models.Index(fields=['instructor']),
        ]

    def __str__(self):
        return f"{self.name} - {self.date_time} ({self.available_slots} slots left)"


# Custom QuerySet for Booking
class BookingQuerySet(models.QuerySet):
    def by_client_email(self, email):
        return self.filter(client_email__iexact=email)

    def for_class(self, fitness_class_id):
        # Optimize with select_related (ForeignKey)
        return self.select_related('fitness_class').filter(fitness_class_id=fitness_class_id)

    def recent(self):
        # Optimize with select_related and ordering
        return self.select_related('fitness_class').order_by('-booking_time')


# Manager for Booking
class BookingManager(models.Manager):
    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)

    def by_client_email(self, email):
        return self.get_queryset().by_client_email(email)

    def for_class(self, fitness_class_id):
        return self.get_queryset().for_class(fitness_class_id)

    def recent(self):
        return self.get_queryset().recent()


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(db_index=True)  # Add index here
    booking_time = models.DateTimeField(auto_now_add=True, db_index=True)  # Add index here

    objects = BookingManager()

    class Meta:
        indexes = [
            models.Index(fields=['client_email']),
            models.Index(fields=['booking_time']),
            models.Index(fields=['fitness_class', 'booking_time']),  # Compound index
        ]

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"
