from rest_framework import serializers
from .models import Listing, Booking, Review, Payment

class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 
            'price_per_night', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    # If your Booking model has a ForeignKey to Listing, you might want to show more than just the ID
    # For example, if you want to show the listing's title:
    # listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'guest', 'check_in_date',
            'check_out_date', 'total_price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_price', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

   


