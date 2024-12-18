"""
Tests of booking: PaymentView changes related to booking feature.
    Changes included in this module: Payment View accessibility depending on users.
"""
import unittest

from django.test import TestCase
from django.urls import reverse
from renthub.models import Room, Renter, Rental


class PaymentViewTests(TestCase):
    """Tests of PaymentView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword',
                                                  phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword',
                                                  phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00)

    def test_payment_access_for_authenticated_renter(self):
        """An authenticated renter can access the payment page."""
        self.client.login(username='renter1', password='testpassword')

        start_date_str = '2024-01'
        end_date_str = '2024-12'
        url = reverse('renthub:payment', kwargs={'room_number': self.room.room_number})
        url_with_params = f"{url}?start_month={start_date_str}&end_month={end_date_str}"

        response = self.client.get(url_with_params)
        self.assertEqual(response.status_code, 200)

    def test_payment_access_for_unauthenticated_user(self):
        """An unauthenticated user cannot access the payment page."""
        start_date_str = '2024-01'
        end_date_str = '2024-12'
        url = reverse('renthub:payment', kwargs={'room_number': self.room.room_number})
        url_with_params = f"{url}?start_month={start_date_str}&end_month={end_date_str}"

        response = self.client.get(url_with_params)
        self.assertEqual(response.status_code, 302)

    def test_payment_access_for_non_owner_renter(self):
        """A renter who tried to view a payment page of a room associated with a rental belonging to another renter
        is redirected to rental page. """
        Rental.objects.create(room=self.room, renter=self.renter1, price=self.room.price)
        self.client.login(username='renter2', password='testpassword')

        start_date_str = '2024-01'
        end_date_str = '2024-12'
        url = reverse('renthub:payment', kwargs={'room_number': self.room.room_number})
        url_with_params = f"{url}?start_month={start_date_str}&end_month={end_date_str}"

        response = self.client.get(url_with_params)
        self.assertEqual(response.status_code, 302)
