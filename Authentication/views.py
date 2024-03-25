from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.core.mail import send_mail
import random
from .models import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from rest_framework.authtoken.models import Token
import google.generativeai as genai

genai.configure(api_key='AIzaSyCHHVhVlcfWQd33H9-CLvBZph41SHn3UsQ')
model = genai.GenerativeModel('gemini-pro')



class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            strategy = load_strategy(request)
            backend = load_backend(strategy=strategy, name='google-oauth2', redirect_uri=None)
            
            # Verify the token and get user info
            user = backend.do_auth(token)
        except (MissingBackend, AuthTokenError, AuthForbidden):
            return Response({'error': 'Invalid token or failed authentication'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user:
            if not user.is_active:
                return Response({'error': 'User account is disabled'}, status=status.HTTP_400_BAD_REQUEST)

            # Optionally, you could handle user.is_verified here

            # Create a token for the user
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'user_id': user.id, 'email': user.email}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)










class CreatorAccountActivationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreatorSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Creator account activated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class UserRegistrationAPIView(APIView):
    def post(self, request):
        print(request.data)
        if User.objects.filter(username=request.data.get('username')).exists():
            messagge = "User with this username already exists"
            return Response({'message':messagge}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if  User.objects.filter(email=request.data.get('email')).exists():
            messagge = "User with this email already exists"
            return Response({'message':messagge}, status=status.HTTP_400_BAD_REQUEST)
        
        username = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        contact = request.data.get('contact_no')
        gender = request.data.get('gender')
        
        if email and password and username and contact:
            user = User.objects.create(username=username, email=email, password=password, contact_no=contact, gender=gender)
            user.set_password(password)
            user.save()
        
            return Response({'message': 'User registered successfully. Please verify your account.','verified':user.is_verified}, status=status.HTTP_201_CREATED)
        else:
            messagge = "Please give correct information"
        return Response({'message':messagge}, status=status.HTTP_400_BAD_REQUEST)

   

class OTPVerificationAPIView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')
        
        try:
            user = User.objects.get(username=email)
            if str(otp)=='1234':
                user.is_verified = True
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': 'Account verified successfully.', 'verified': user.is_verified,'token':token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        email = request.data.get('email')
        
        try:
            user = User.objects.get(username=email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            send_mail(
                'Verify your account',
                f'Your OTP is {otp}.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent via email.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)



   
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            user = User.objects.get(email=request.data.get('email'))
            if user.is_verified:
                return Response({'token': token.key,'verified':user.is_verified}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Please Verify Your account','verified':user.is_verified}, status=status.HTTP_200_OK)
        return Response({'message':'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        user = User.objects.get(email=request.user.email)
        user.username = request.data.get('username', user.username)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.contact_no = request.data.get('phone_number', user.contact_no)
        user.address = request.data.get('address', user.address)
        user.gender = request.data.get('gender', user.gender)
        user.save()
        
            
        return Response({'data':UserProfileUpdateSerializer(user).data}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def verify_mail(request):
    if request.method == 'POST':
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'message':'Email Exist','check':True},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Email doest not Exist','check':False},status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST','PUT'])
def forgot_password(request):
    if request.method == 'POST':
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
        
    if request.method == 'PUT':
        otp = request.data.get('otp')
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if str(otp)=='1234':
                user.is_verified = True
                user.set_password(password)
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': 'Account verified successfully.', 'verified': user.is_verified,'token':token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
       
        return Response({'message':'Email doest not Exist'},status=status.HTTP_400_BAD_REQUEST)
    



import re
from DesignGenerator.models import  *
@api_view(['POST'])
def suggestions(request):
    # prompt = request.data.get('prompt')
    # response = model.generate_content(f"I want to generate image which i want print it on cloths. For that give suggestion for prompts and also give list of tags. The starting prompt is :{prompt} ")
    
    prompt = request.data.get('prompt')
    suggestion = model.generate_content(f"I want to generate image which i want print it on cloths. For that give suggestion for prompt. Note please provide ',' seperated . The starting prompt is :{prompt} ")

    prompt = request.data.get('prompt')
    tags = model.generate_content(f"I want to generate image which i want print it on cloths. For that give tags. Note please provide ',' seperated . The starting prompt is :{prompt} ")

   
    
    return Response({'suggestion':suggestion.text,'tags':tags.text.split(',')},status=status.HTTP_200_OK)





@api_view(["GET"])
def filter_by_tags(request):
    pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def virtually_tried(request):
    user = request.user
    vtried = VirtuallyTried.objects.filter(user=user)
    data = VirtuallyTriedSerializer(vtried, many=True).data
    return Response(data, status=status.HTTP_200_OK)

@api_view(["POST"])
def waitlist(request):
    if request.method == 'POST':
        email = request.data.get('email')
        print(email)
        if Waitlist.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists in waitlist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Waitlist.objects.create(email=email).save()
            print("!!!!!!!!1")
            return Response({'message': 'Email added to waitlist'}, status=status.HTTP_200_OK)
            