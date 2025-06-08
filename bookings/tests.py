from django.test import TestCase
from .models import FitnessClass

class FitnessClassTestCase(TestCase):
    def setUp(self):
        FitnessClass.objects.create(
            name='Yoga',
            date_time='2025-06-10T10:00:00Z',
            instructor='Ankit',
            available_slots=5
        )

    def test_class_created(self):
        yoga_class = FitnessClass.objects.get(name='Yoga')
        self.assertEqual(yoga_class.instructor, 'Ankit')
        self.assertEqual(yoga_class.available_slots, 5)
