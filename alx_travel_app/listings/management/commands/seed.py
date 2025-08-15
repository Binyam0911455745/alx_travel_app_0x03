# ~/alx_travel_app_0x00/alx_travel_app/listings/management/commands/seed.py

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
import random
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with sample data for Listings, Bookings, and Reviews.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        self.stdout.write('Clearing existing data...')
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()

        if not User.objects.exists():
            self.stdout.write('Creating a superuser for testing...')
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            User.objects.create_user('guest1', 'guest1@example.com', 'guestpassword')
            User.objects.create_user('guest2', 'guest2@example.com', 'guestpassword')
        else:
            self.stdout.write('Users already exist, skipping user creation.')

        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create at least one user (e.g., via manage.py createsuperuser) before running the seeder.'))
            return

        listings_data = [
            {
                'title': 'Cozy Apartment in City Center',
                'description': 'A beautiful and cozy apartment right in the heart of the city.',
                'address': '123 Main St',
                'city': 'New York',
                'country': 'USA',
                'price_per_night': 150.00,
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 1,
                'amenities': 'Wifi,Kitchen,TV,Air Conditioning',
            },
            {
                'title': 'Spacious Family House with Garden',
                'description': 'Perfect for families, with a large garden and close to parks.',
                'address': '456 Oak Ave',
                'city': 'Los Angeles',
                'country': 'USA',
                'price_per_night': 250.00,
                'max_guests': 8,
                'bedrooms': 4,
                'bathrooms': 2,
                'amenities': 'Wifi,Parking,Garden,BBQ,Washer',
            },
            {
                'title': 'Beachfront Villa with Ocean View',
                'description': 'Stunning villa with direct beach access and breathtaking views.',
                'address': '789 Ocean Dr',
                'city': 'Miami',
                'country': 'USA',
                'price_per_night': 400.00,
                'max_guests': 6,
                'bedrooms': 3,
                'bathrooms': 3,
                'amenities': 'Wifi,Pool,Beach Access,Balcony',
            },
            {
                'title': 'Rustic Cabin in the Woods',
                'description': 'Escape to nature in this charming, secluded cabin.',
                'address': '101 Forest Rd',
                'city': 'Asheville',
                'country': 'USA',
                'price_per_night': 120.00,
                'max_guests': 2,
                'bedrooms': 1,
                'bathrooms': 1,
                'amenities': 'Fireplace,Hiking Trails,Pet-friendly',
            },
            {
                'title': 'Modern Loft in Downtown',
                'description': 'Stylish loft with city views, ideal for solo travelers or couples.',
                'address': '222 Tech St',
                'city': 'San Francisco',
                'country': 'USA',
                'price_per_night': 180.00,
                'max_guests': 2,
                'bedrooms': 1,
                'bathrooms': 1,
                'amenities': 'Wifi,Gym,Elevator,City View',
                'is_active': False
            }
        ]

        created_listings = []
        with transaction.atomic():
            for data in listings_data:
                listing = Listing.objects.create(**data)
                created_listings.append(listing)
                self.stdout.write(self.style.SUCCESS(f'Created Listing: {listing.title}'))

        bookings_to_create = []
        today = date.today()

        if created_listings:
            for i in range(5):
                listing = random.choice(created_listings)
                guest = random.choice(users)
                check_in_date = today + timedelta(days=random.randint(5, 30))
                check_out_date = check_in_date + timedelta(days=random.randint(2, 7))
                total_price = (check_out_date - check_in_date).days * float(listing.price_per_night) # Cast to float for multiplication
                status = random.choice([Booking.BookingStatus.PENDING, Booking.BookingStatus.CONFIRMED, Booking.BookingStatus.COMPLETED])

                bookings_to_create.append(
                    Booking(
                        listing=listing,
                        guest=guest,
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                        total_price=total_price,
                        status=status
                    )
                )
            Booking.objects.bulk_create(bookings_to_create)
            self.stdout.write(self.style.SUCCESS(f'Created {len(bookings_to_create)} Bookings.'))
        else:
            self.stdout.write(self.style.WARNING('No listings created, skipping booking seeding.'))

        completed_bookings = Booking.objects.filter(status=Booking.BookingStatus.COMPLETED)
        reviews_to_create = []

        with transaction.atomic():
            for booking in completed_bookings:
                if not Review.objects.filter(booking=booking).exists():
                    rating = random.randint(3, 5)
                    comment = random.choice([
                        "Great stay!",
                        "Highly recommended.",
                        "Clean and comfortable.",
                        "Excellent location.",
                        "Enjoyed my time here.",
                        ""
                    ])
                    reviews_to_create.append(
                        Review(
                            booking=booking,
                            guest=booking.guest,
                            rating=rating,
                            comment=comment
                        )
                    )
            if reviews_to_create:
                Review.objects.bulk_create(reviews_to_create)
                self.stdout.write(self.style.SUCCESS(f'Created {len(reviews_to_create)} Reviews for completed bookings.'))
            else:
                self.stdout.write(self.style.WARNING('No completed bookings to review, skipping review seeding.'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
