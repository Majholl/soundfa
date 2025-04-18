from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework import status
from loguru import logger
from typing import Optional
from django.conf import settings
from os import path
import os
from ..manager import validate_email_address

from ..serializers.users_serializers import RegisterSerializer, LoginSerializer
from ..cookies import set_auth_cookies



User = get_user_model()




@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
        -This function add's user into the database by registering them
        #- METHOD : POST
        #- data scheme : {'first_name':User-firstname, 'last_name':User-lastname, 'username':User-username, 'email':User-email, 'password':User-password}
        
    """
    data = request.data
    
    try:
        
        if not 'username' in data:
            return Response({'msg':'Provide username for registeration.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'email' in data:
            return Response({'msg':'Provide email address for registeration.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'email' and not validate_email_address(data['email']):
            return Response({'msg':'Email address is not valid.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'password' in data:
            return Response({'msg':'Provide password for registeration.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
         
        if User.objects.filter(username=data['username']).exists():
            return Response({'msg':'User with this username exists.', 'status':302}, status=status.HTTP_302_FOUND)

        
        if User.objects.filter(email=data['email']).exists() :
            return Response({'msg':'User with this email exists.', 'status':302}, status=status.HTTP_302_FOUND)
    
    
        serializer = RegisterSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            tokens = RefreshToken.for_user(user)
            
            return Response({'msg':'User registered successfully', 'user':serializer.data, 'refresh':str(tokens), 'access':str(tokens.access_token)}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
        -This function login  user into the system by login them
        #- METHOD : POST
        #- data scheme : {'username':User-username, 'email':User-email, 'password':User-password}
        
    """
    data = request.data
    
    try:
        if not ( 'username' in data or 'email' in data)  :
            return Response({'msg':'Provide username or email address.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'username' in data and 'email' in data:
            return Response({'msg':"Provide username or email address not both.", 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'username' in data and not User.objects.filter(username=data['username']).exists():
            return Response({'msg':'User with this username does not exists.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
                
        if 'email' in data and not User.objects.filter(email=data['email']).exists():
            return Response({'msg':'User with this email address does not exists.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
        if not 'password' in data:
            return Response({'msg':'Provide a password.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data

            tokens = RefreshToken.for_user(user['id'])
            info = {'id':user['id'].pk, 'username':user['id'].username, 'email':user['id'].email, }
            resp = Response({'msg':'User logged in successfully', 'status':200, 'user':info, 'refresh':str(tokens), 'access':str(tokens.access_token)}, status=status.HTTP_200_OK)
            set_auth_cookies(resp, tokens.access_token, tokens)
            return resp
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
        -This function refresh user token 
        #- METHOD : POST
           
    """
    try:
        
        refresh_token = request.COOKIES.get('refresh')
        
        if not refresh_token :
            return Response({'msg':'Refresh token not found, login first.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        new_tokens = RefreshToken(refresh_token)
        resp = Response({'message': 'Token refreshed successfully', 'status':200, 'refresh':str(new_tokens), 'access':str(new_tokens.access_token)}, status=status.HTTP_200_OK)
        set_auth_cookies(resp, new_tokens.access_token, new_tokens)
        return resp
        

    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['POST'])
@permission_classes([AllowAny])
def logout_user(request):
    """
        -This function logout the user
        #- METHOD : POST
           
    """
    try:
        
        resp = Response({'msg':'User logout successfully.', 'status':204}, status=status.HTTP_204_NO_CONTENT)
        resp.delete_cookie('logged_in')
        resp.delete_cookie('access')
        resp.delete_cookie('refresh')
        return resp
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
