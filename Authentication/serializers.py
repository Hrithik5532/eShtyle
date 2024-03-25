from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('gender', 'contact_no', 'address', 'email','username','is_creator','is_verified','full_body_image')
        
        

    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','otp')




from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")



class CreatorSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer()
    class Meta:
        model = Creator
        fields = [ 'bank_details', 'ifsc_code', 'id_proof', 'payment_made']

    def validate(self, data):
        # Check if creating a creator account
            required_fields = ['bank_details', 'ifsc_code', 'id_proof', 'payment_made']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            if missing_fields:
                raise serializers.ValidationError({field: "This field is required." for field in missing_fields})
            
            # Additional checks can go here (e.g., format validation)

            return data

    def update(self, instance, validated_data):
        instance.user.is_creator = validated_data.get('is_creator', instance.user.is_creator)
        instance.bank_details = validated_data.get('bank_details', instance.bank_details)
        instance.ifsc_code = validated_data.get('ifsc_code', instance.ifsc_code)
        instance.id_proof = validated_data.get('id_proof', instance.id_proof)
        instance.payment_made = validated_data.get('payment_made', instance.payment_made)
        
        instance.save()
        return instance
    
    

class VirtuallyTriedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtuallyTried
        fields = '__all__'