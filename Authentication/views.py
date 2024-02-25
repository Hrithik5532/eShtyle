from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, LoginSerializer
from django.core.mail import send_mail
import random
from .models import User

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_verified = False  # Set the user as unverified initially
            user.save()
            
            return Response({'message': 'User registered successfully. Please verify your account.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OTPVerificationAPIView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        user = User.objects.get(email=request.user.email)
        # Retrieve the user and OTP from your database or cache
        if int(otp)== user.otp:  # Implement this function based on how you store OTPs
            user.is_verified = True
            user.save()
            return Response({'message': 'Account verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
            user = User.objects.get(email=request.user.email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            # Generate a 6-digit OTP
            # Here, save the OTP to your database or cache with an expiration time
            # For email:
                # send_mail(
                #     'Verify your account',
                #     f'Your OTP is {otp}.',
                #     'hrithikhadawale75@gmail.com',  # Update with your email
                #     [user.email],
                #     fail_silently=False,
                # )
            # If using SMS, integrate with your SMS provider to send the OTP
            return Response({'message': 'OTP Sent on mail'}, status=status.HTTP_200_OK)
        
        
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            user = User.objects.get(email=request.data.get('email'))
            if user.is_verified:
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Please Verify Your account','verified':False}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)