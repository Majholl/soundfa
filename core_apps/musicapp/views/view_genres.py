from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from urllib.request import Request
from loguru import logger
from typing import Optional
from django.conf import settings
from rest_framework import status
from os import path



from ..models.albums import AlbumModel 
from ..models.artists import ArtistsModel
from ..models.musics import MusicModel
from ..models.genres import GenereModel
from ..serializers.generes_serializers import CreateGenreSerializers, GetAllGenereSerializers
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin, Is_superadmin 








@api_view(['POST'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_genere(request):
    data = request.data
    try:
        
        if len(data) < 1 :
            return Response({'msg':'Add this fields to add genere.', 'essential-field':'name, generecover', 'optional-fields':'artist_id, music_idو album_id, description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'name' not in data or ('name' in data and all(name.strip()=='' for name in data['name'])):
            return Response({'msg':'Provide a name for the genere.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'generecover' in data:
            if len(data['generecover']) == 0 or len(data.getlist('generecover')) > 1 :
                return Response({'msg':'One album cover must be provided.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['generecover'].name)[-1] not in ['.jpg', '.jpeg', '.png']:
                 return Response({'msg':'This music type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)


        serializer = CreateGenreSerializers(data=data)        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Genere addedd successfully.', 'status':201, 'data':serializer.data}, status=status.HTTP_201_CREATED)
    
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  
  
  
  
  
  
  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_genere(request):
    data = request.data
    try:    

        playlists = GenereModel.objects.all()
        
        serializers = GetAllGenereSerializers(instance=playlists, many=True)
        return Response({'msg':'All the generes.', 'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    
    
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_genere(request):
    data = request.data
    try:    
        if not 'genere_id' in data:
            return Response({'msg':'Provide genere id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        playlists = GenereModel.objects.get(pk=data['genere_id'])
        
        serializers = GetAllGenereSerializers(instance=playlists)
        return Response({'msg':'All the genere.', 'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
      
      
      

@api_view(['DELETE'])
@permission_classes([Is_superadmin])
def delete_genere(request):
    data = request.data
    
    try:
        
        if not 'genere_id' in data:
            return Response({'msg':'Provide genere id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        genere = GenereModel.objects.get(id=data['genere_id'])
        
        genere.artist_id.clear()
        genere.music_id.clear()
        genere.album_id.clear()
        genere.delete()
        return Response({'msg':'Genere Removed successfully.', 'status':201}, status=status.HTTP_201_CREATED)
    
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
