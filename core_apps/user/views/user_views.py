from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken 

from loguru import logger
from django.utils import timezone
from django.conf import settings
from os import path
import os , random


from ..emails import send_reset_password_code
from ..serializers.users_serializers import RegisterUserSerializer, UpdateUserSerializer, GetMeUserSerializer
from ..manager import validate_email_address
from ..cookies import set_auth_cookies



User = get_user_model()




@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
        - Register user with given values.
        - METHOD : POST
        - Token type : bearer
        - Json schema:{"first_name":"test",  "last_name":"test",  "username":"test, "email":"test@gmail.com", "password":"test"}   
    """
    
    data = request.data
    
    try:
        
        if not 'username' in data:
            return Response({'msg':'Provide username for registeration.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'email' in data:
            return Response({'msg':'Provide email address for registeration.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'email' in data and not validate_email_address(data['email']):
            return Response({'msg':'Email address is not valid.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'password' in data:
            return Response({'msg':'Provide password for registeration.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
         
        if User.objects.filter(username=data['username']).exists():
            return Response({'msg':'User with this username exists.', 'status':302}, status=status.HTTP_302_FOUND)

        
        if User.objects.filter(email=data['email']).exists() :
            return Response({'msg':'User with this email exists.', 'status':302}, status=status.HTTP_302_FOUND)
    
        serializer = RegisterUserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            logger.info(f'New user registred. {str(serializer.data)}')
            resp = Response({'msg':'User registered successfully.', 'status':201, 'data':serializer.data}, status=status.HTTP_201_CREATED)
            set_auth_cookies(resp, serializer.data['access'], serializer.data['refresh'])
            return  resp
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
        - Login user with given values.
        - METHOD : POST
        - Set cookies for user
        - Json schema: {"username":"test, "email":"test@gmail.com", "password":"test"}       
    """
    data = request.data
    
    try:
        lookup = {}

        if 'email' not in data:
            return Response({'msg':'Provide email address or username for loging.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'email' in data and any(email.strip()=='' for email in data['email']):
            return Response({'msg':'email field can not be empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'password' not in data:
            return Response({'msg':'Provide a password.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'password' in data and any(passwd.strip() =='' for passwd in data['password']):
            return Response({'msg':'password field can not be empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if validate_email_address(data['email']):
            lookup['email'] = data['email']
        else:   
            lookup['username'] = data['email']
        
        user = User.objects.get(**lookup)
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            if not user.check_password(data['password']):
                return Response({'msg':'passowrd is not correct.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            tokens = RefreshToken.for_user(user)
            info = {'id':str(user.pk), 'first_name':str(user.first_name), 'last_name':str(user.last_name), 'username':str(user.username), 'email':str(user.email), 'refresh':str(tokens), 'access':str(tokens.access_token), 'last_login':str(user.last_login), 'created_at':str(user.created_at), 'updated_at':str(user.updated_at)}
            resp = Response({'msg':'User logged in successfully', 'status':200, 'data':info}, status=status.HTTP_200_OK)
            set_auth_cookies(resp, info['access'], info['refresh'])
            return resp
        
        
        return Response({'msg':'An error occured.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except User.DoesNotExist :
        return Response({'msg':'User with this email or username does not exists.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
        - Refresh user access and refresh both token.
        - METHOD : POST
        - Set cookies for user
    """
    try:
        refresh_token = request.COOKIES.get('refresh')
        
        if not refresh_token :
            return Response({'msg':'Refresh token not found, login first.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        new_tokens = RefreshToken(refresh_token)
        if new_tokens:
            resp = Response({'msg': 'Token refreshed successfully', 'status':202, 'refresh':str(new_tokens), 'access':str(new_tokens.access_token)}, status=status.HTTP_202_ACCEPTED)
            set_auth_cookies(resp, new_tokens.access_token, new_tokens)
            return resp
        
        return Response({'msg':'An error occured.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)    

    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
        - Update the user data.
        - METHOD : PUT
        - json schema : {"first_name":"test, "last_name":"test", "profile":"image"}     
    """
    data = request.data
    user = request.user
    try:
        if len(data) < 1 :
            return Response({'msg':'To update user data provide a value.', 'optional-fields':'first_name, last_name, profile', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'profile' in data: 
            if len(data['profile']) == 0 or len(data.getlist('profile')) >1 :
                return Response({'msg':'only one profile is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['profile'].name)[-1] not in ['.jpg', '.png', '.jpeg']:
                return Response({'msg':'This file type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = UpdateUserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            if 'profile' in data:
                image_path = path.join(settings.MEDIA_ROOT, user.profile.path)
                if os.path.exists(image_path):
                    os.remove(image_path)
            serializer.save()
            return Response({'msg':'User info updated successfully.', 'status':200, 'data': serializer.data}, status=status.HTTP_200_OK)
                
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
        
    except Exception as err:
        return Response({'msg': 'Internal server error.', 'status': 500, 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
         




@api_view(['POST'])
def reset_password(request):
    data = request.data
    user = request.user
    
    try:
       
        code = f'{random.randint(000000,999999)}'
        
        if 'email' in data and not user.is_authenticated: 
            user = User.objects.get(email= data['email'])
            
        if user.is_authenticated : 
            send_reset_password_code.delay(user.email, user.username, code)
            user.resest_password= code
            user.save()
            return Response({'msg':'Reset code sent.', 'user':user.email, 'status':200}, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'msg':'User with this email does not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND) 
       
    except Exception as err:
        return Response({'msg': 'Internal server error.', 'status': 500, 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def reset_password_confirm(request):
    data = request.data
    user = request.user
    
    try:
       
        if 'email' not in data or 'code' not in data or 'password' not in data :
            return Response({'msg':'email or code or password is not provided.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email= data['email'])
        if str(user.resest_password) != str(data['code']):
                return Response({'msg':'Your code is wrong.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(data['password'])
        user.resest_password = ""
        user.save()
        return Response({'msg':'Your password reseted successfully.', 'user':user.email, 'status':200}, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'msg':'User with this email does not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND) 
       
    except Exception as err:
        return Response({'msg': 'Internal server error.', 'status': 500, 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me_user(request):
    """
        - return the user data.
        - METHOD : GET      
    """
    user = request.user
    try:
        serializer = GetMeUserSerializer(instance=user)
        return Response({'msg': 'User information found successfully.', 'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)

    except Exception as err:
        return Response({'msg': 'Internal server error.', 'status': 500, 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
 
 
 
 




@api_view(['POST'])
@permission_classes([AllowAny])
def logout_user(request):
    """
        - Logout the user.
        - METHOD : POST
        - Clear cookies of the user       
    """
    try:
        
        resp = Response({'msg':'User logout successfully.', 'status':204}, status=status.HTTP_204_NO_CONTENT)
        resp.delete_cookie('logged_in')
        resp.delete_cookie('access')
        resp.delete_cookie('refresh')
        if resp:
            return resp
    
        return Response({'msg':'An error occured.', 'status':400,}, status=status.HTTP_400_BAD_REQUEST)    

    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)