from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from urllib.request import Request
from loguru import logger
from typing import Optional
from django.conf import settings
from rest_framework import status
import os 
from os import path

from ..serializers.playlists_serializers import GetAllListsSerializers
from ..models.albums import AlbumModel 
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin , Is_superadmin


User = get_user_model()




@api_view(['POST'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_playlist(request):
    data = request.data
    user = request.user
    
    try:
        
        if not 'album_id' in data:
            return Response({'msg':'Provide Album id for the user.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        album = AlbumModel.objects.get(id=data['album_id'])
        
        user.playlists.add(album.pk)
        return Response({'msg':'playlist added successfully.', 'status':201}, status=status.HTTP_201_CREATED)
    
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Album does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_playlist_user(request):
    user = request.user
    try:    
        albums_id = user.playlists.values_list('id', flat=True)
        playlists = AlbumModel.objects.filter(pk__in=albums_id).all()
        serializers = GetAllListsSerializers(instance=playlists, many=True)
        return Response({'msg':'All the playlists.', 'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    
    
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_playlist_user(request):
    data = request.data
    user = request.user
    try:    
        if not 'album_id' in data:
            return Response({'msg':'Provide Album id for the user.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        playlists = AlbumModel.objects.get(pk=data['album_id'])
        
        serializers = GetAllListsSerializers(instance=playlists)
        return Response({'msg':'All the playlists.', 'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Album does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    
    
    
    
    
    

@api_view(['DELETE'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def delete_playlist(request):
    data = request.data
    user = request.user
    try:
        
        if not 'album_id' in data:
            return Response({'msg':'Provide Album id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        album = AlbumModel.objects.get(id=data['album_id'])
        user.playlists.remove(album)
        album.delete()
        return Response({'msg':'playlist Removed successfully.', 'status':201}, status=status.HTTP_201_CREATED)
    
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Album does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
