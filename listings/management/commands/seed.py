from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from datetime import date, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')
        
        # Create users
        self.create_users()
        
        # Create listings
        self.create_listings()
        
        # Create bookings
        self.create_bookings()
        
        # Create reviews
        self.create_reviews()
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))

    def create_users(self):
        """Create sample users."""
        users_data = [
            {'username': 'host1', 'email': 'host1@example.com', 'first_name': 'John', 'last_name': 'Host'},
            {'username': 'host2', 'email': 'host2@example.com', 'first_name': 'Jane', 'last_name': 'Host'},
            {'username': 'guest1', 'email': 'guest1@example.com', 'first_name': 'Mike', 'last_name': 'Guest'},
            {'username': 'guest2', 'email': 'guest2@example.com', 'first_name': 'Sarah', 'last_name': 'Guest'},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')

    def create_listings(self):
        """Create sample listings."""
        hosts = User.objects.filter(username__in=['host1', 'host2'])
        
        listings_data = [
            {
                'title': 'Cozy Downtown Apartment',
                'description': 'Beautiful apartment in city center',
                'location': 'New York, NY',
                'price_per_night': Decimal('150.00'),
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 1,
                'amenities': 'WiFi, Kitchen, AC',
            },
            {
                'title': 'Beach House Villa',
                'description': 'Stunning beachfront property',
                'location': 'Miami, FL',
                'price_per_night': Decimal('300.00'),
                'max_guests': 8,
                'bedrooms': 4,
                'bathrooms': 3,
                'amenities': 'Pool, Beach Access, WiFi',
            },
            {
                'title': 'Mountain Cabin',
                'description': 'Peaceful retreat in the mountains',
                'location': 'Denver, CO',
                'price_per_night': Decimal('200.00'),
                'max_guests': 6,
                'bedrooms': 3,
                'bathrooms': 2,
                'amenities': 'Fireplace, Kitchen, Hot Tub',
            }
        ]
        
        for i, listing_data in enumerate(listings_data):
            host = hosts[i % len(hosts)]
            available_from = date.today() + timedelta(days=1)
            available_to = available_from + timedelta(days=365)
            
            listing, created = Listing.objects.get_or_create(
                title=listing_data['title'],
                defaults={
                    **listing_data,
                    'host': host,
                    'available_from': available_from,
                    'available_to': available_to,
                }
            )
            
            if created:
                self.stdout.write(f'Created listing: {listing.title}')

    def create_bookings(self):
        """Create sample bookings."""
        guests = User.objects.filter(username__in=['guest1', 'guest2'])
        listings = Listing.objects.all()
        
        for listing in listings[:2]:
            for guest in guests:
                start_date = date.today() + timedelta(days=random.randint(30, 60))
                end_date = start_date + timedelta(days=random.randint(3, 10))
                duration = (end_date - start_date).days
                total_price = listing.price_per_night * duration
                
                booking, created = Booking.objects.get_or_create(
                    listing=listing,
                    user=guest,
                    start_date=start_date,
                    defaults={
                        'end_date': end_date,
                        'total_price': total_price,
                        'status': 'confirmed',
                    }
                )
                
                if created:
                    self.stdout.write(f'Created booking: {booking.booking_id}')

    def create_reviews(self):
        """Create sample reviews."""
        guests = User.objects.filter(username__in=['guest1', 'guest2'])
        listings = Listing.objects.all()
        
        comments = [
            "Great place to stay!",
            "Amazing location and host.",
            "Clean and comfortable.",
            "Exceeded expectations!",
        ]
        
        for listing in listings:
            for guest in guests:
                review, created = Review.objects.get_or_create(
                    listing=listing,
                    user=guest,
                    defaults={
                        'rating': random.randint(4, 5),
                        'comment': random.choice(comments),
                    }
                )
                
                if created:
                    self.stdout.write(f'Created review for: {listing.title}')