from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken 
from time import time
from django.conf import settings


from ..utils import generate_code

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    """
        - Serializer for registering user and validating data 
        - based on : User model
        - METHOD : POST
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password',]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        
        if settings.OTP_REQUIRED == "True":
            user.set_otp(generate_code())
        else:
            user.account_status = user.AccountStatus.ACTIVE 
            user.is_active = 1
            user.save()
            
        if user:
            return user


    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        return req






class UpdateUserSerializer(serializers.ModelSerializer):
    """
        - Serializer for updating user data
        - based on : User model
        - METHOD : POST
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile']
 
    def update(self, instance, validated_data):
        try:
            
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.upated_at = int(time())
            instance.save()
            
            return instance
        
        except Exception as err:
            pass
        
    def to_representation(self, instance):
        req =super().to_representation(instance)  
        req['username'] = instance.username
        req['email'] = instance.email 
        req['created_at'] = instance.created_at
        req['updaetd_at'] = instance.updated_at
        return req







class GetMeUserSerializer(serializers.ModelSerializer):
    """
        - Serializer for return user data
        - based on : User model
        - METHOD : GET
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'usertype', 'is_active', 'is_superuser', 'is_staff', 'last_login', 'created_at', 'updated_at']

