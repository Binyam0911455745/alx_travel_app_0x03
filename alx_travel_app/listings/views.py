# ~/alx_travel_app_0x02/alx_travel_app/listings/views.py

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
import uuid
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer

# --- Listing ViewSet ---
class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed, created, updated or deleted.
    """
    queryset = Listing.objects.all().order_by('title')
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # You might add custom logic here, e.g., to filter listings by owner for write operations
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user) # If Listing has an 'owner' field

# --- Booking ViewSet ---
class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed, created, updated or deleted.
    """
    queryset = Booking.objects.all().order_by('-check_in_date')
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Example: Filter bookings to only show current user's bookings (for list and retrieve)
    def get_queryset(self):
        # If the user is an admin, they can see all bookings
        if self.request.user.is_staff:
            return Booking.objects.all()
        # Otherwise, only show bookings where they are the guest
        return Booking.objects.filter(guest=self.request.user).order_by('-start_date')

    # Example: Automatically set the guest for new bookings to the current user
    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

# -----------------------------------------------------------------------------
# New API Views for Chapa Payment Integration
# -----------------------------------------------------------------------------

@method_decorator(csrf_exempt, name='dispatch')
class PaymentInitiationView(APIView):
    # Allow any user, authenticated or not, to access this endpoint
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Initiates a payment with Chapa.
        """
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'ETB')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        tx_ref = f"tx-{uuid.uuid4()}"

        data = {
            "amount": amount,
            "currency": currency,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "tx_ref": tx_ref,
            "callback_url": f"https://your-domain.com/api/v1/payments/verify/{tx_ref}/"
        }

        headers = {
            "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}",
            "Content-Type": "application/json"
        }
        
        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        try:
            response = requests.post(chapa_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            chapa_data = response.json()
        except requests.exceptions.RequestException as e:
            # CORRECTED: Handle different HTTP error codes from the Chapa API.
            if e.response is not None and e.response.status_code == 400:
                # Return the error message directly from Chapa if it's a 400 Bad Request.
                return Response({"error": "Bad Request to Chapa API.", "details": e.response.json()}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Failed to connect to Chapa API.", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if chapa_data.get("status") == "success":
            payment_record = Payment.objects.create(
                booking_reference=tx_ref,
                amount=amount,
                status='pending'
            )
            serializer = PaymentSerializer(payment_record)
            
            return Response({
                "message": chapa_data.get("message"),
                "checkout_url": chapa_data.get("data").get("checkout_url"),
                "tx_ref": tx_ref,
                "payment_details": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": chapa_data.get("message")}, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerificationView(APIView):
    # Allow any user, authenticated or not, to access this endpoint
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, transaction_id, *args, **kwargs):
        """
        Verifies a payment with Chapa using the transaction ID.
        """
        headers = {
            "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}",
        }
        
        chapa_url = f"https://api.chapa.co/v1/transaction/verify/{transaction_id}"
        
        try:
            response = requests.get(chapa_url, headers=headers)
            response.raise_for_status()
            chapa_data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to connect to Chapa API.", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if chapa_data.get("status") == "success":
            try:
                payment = Payment.objects.get(booking_reference=transaction_id)
                payment.status = 'completed'
                payment.transaction_id = chapa_data.get("data").get("id")
                payment.save()
                
                serializer = PaymentSerializer(payment)
                return Response({
                    "message": "Payment verified successfully.",
                    "payment_details": serializer.data
                }, status=status.HTTP_200_OK)
            except Payment.DoesNotExist:
                return Response({"error": "Payment record not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If verification fails, update the payment status to failed
            try:
                payment = Payment.objects.get(booking_reference=transaction_id)
                payment.status = 'failed'
                payment.save()
            except Payment.DoesNotExist:
                pass # The payment record might not exist, so we just ignore

            return Response({"error": chapa_data.get("message")}, status=status.HTTP_400_BAD_REQUEST)