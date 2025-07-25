from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model."""
    
    host = UserSerializer(read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'title', 'description', 'location',
            'price_per_night', 'available_from', 'available_to',
            'max_guests', 'bedrooms', 'bathrooms', 'amenities',
            'host', 'created_at', 'updated_at'
        ]
        read_only_fields = ['listing_id', 'host', 'created_at', 'updated_at']

    def validate_price_per_night(self, value):
        """Validate price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate(self, data):
        """Validate date range."""
        available_from = data.get('available_from')
        available_to = data.get('available_to')
        
        if available_to and available_from and available_to <= available_from:
            raise serializers.ValidationError("Available to date must be after available from date.")
        
        return data


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""
    
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing', 'user', 'start_date', 'end_date',
            'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['booking_id', 'user', 'created_at']

    def validate(self, data):
        """Validate booking dates."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if end_date and start_date and end_date <= start_date:
            raise serializers.ValidationError("End date must be after start date.")
        
        return data