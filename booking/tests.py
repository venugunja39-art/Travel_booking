from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import TravelOption, Booking
from django.urls import reverse
from datetime import datetime, timedelta

class TravelBookingTests(TestCase):

    def setUp(self):
        """Setup data before each test"""
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        # Create a travel option
        self.travel = TravelOption.objects.create(
            type="Flight",
            source="Hyderabad",
            destination="Delhi",
            date_time=datetime.now() + timedelta(days=1),
            price=5000,
            available_seats=50
        )
        
        # Create client for HTTP requests
        self.client = Client()

    def test_user_registration(self):
        """Test user registration works"""
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login(self):
        """Test login with correct credentials"""
        login = self.client.login(username="testuser", password="testpass")
        self.assertTrue(login)

    def test_travel_option_created(self):
        """Test Travel Option model"""
        self.assertEqual(self.travel.source, "Hyderabad")
        self.assertEqual(self.travel.destination, "Delhi")
        self.assertEqual(self.travel.available_seats, 50)

    def test_booking_creation(self):
        """Test booking seats works"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("book_travel", args=[self.travel.id]), {
            "number_of_seats": 2
        })
        self.assertEqual(response.status_code, 302)  # Redirect after booking
        booking = Booking.objects.get(user=self.user, travel_option=self.travel)
        self.assertEqual(booking.number_of_seats, 2)
        self.assertEqual(booking.total_price, self.travel.price * 2)

    def test_booking_seat_validation(self):
        """Test booking fails if seats are more than available"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("book_travel", args=[self.travel.id]), {
            "number_of_seats": 100  # More than available
        })
        # Page reloads with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not enough seats available.")
