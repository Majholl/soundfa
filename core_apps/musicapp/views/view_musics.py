from urllib.request import Request
from django.http import FileResponse, Http404
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from loguru import logger
from os import path
import os
from typing import Optional
from django.conf import settings

from ..models.artists import ArtistsModel
from ..models.musics import MusicModel
from ..serializers.musics_serializers import CreateMusicSerializer, UpdateMusicSerializer , GetMusicByNameSerializer
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin , Is_superadmin





@api_view(['GET'])
def get_music_by_musicname(request:Request, name:Optional[str]=None) -> Response:
    """
        - Get music data from db 
        - METHOD : Get
        - Json schema : -
    """
    data = request.data
    
    try:

        info_dict = {}
        
        if name is not None:
            info_dict['title'] = name
        else:
            title_error =  Response({'msg':'Need music title to search for.', 'stats':400}, status=status.HTTP_400_BAD_REQUEST)
            if not 'title' in data:
                return title_error
            
            if 'title' in data and len(data['title']) <1:
                return title_error
                
            info_dict['title'] = data['title']
        
        music = MusicModel.objects.filter(**info_dict)
        
        if music.count() == 0 :
            return Response({'msg':'No musci  found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GetMusicByNameSerializer(instance=music , many=True, context={'request':request})
        return Response({'msg':'Music data found successfully.', 'status':200, 'data':serializer.data, 'total':music.count()}, status=status.HTTP_200_OK)
    
    
    except ArtistsModel.DoesNotExist :
        return Response({'msg':'artist not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except MusicModel.DoesNotExist :
        return Response({'msg':'music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
         
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














@api_view(['GET'])
def get_music_by_artistname(request:Request, name:Optional[str]=None) -> Response:
    """
        - Get music data from db 
        - METHOD : Get
        - Json schema : -
    """
    data = request.data
    
    try:

        info_dict = {}
        
        if name is not None:
            info_dict['name'] = name
        else:
            name_error =  Response({'msg':'Need artist name to search for it\'s musics.', 'stats':400}, status=status.HTTP_400_BAD_REQUEST)
            if not 'name' in data:
                return name_error
            
            if 'name' in data and len(data['name']) <1:
                return name_error
                
            info_dict['name'] = data['name']
            
        artist = ArtistsModel.objects.get(**info_dict)
        music = MusicModel.objects.filter(artist_id = artist.pk)
        if music.count() == 0 :
            return Response({'msg':'Musci not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GetMusicByNameSerializer(instance=music , many=True, context={'request':request})
        return Response({'msg':'Music data found successfully.', 'status':200, 'data':serializer.data, 'total':music.count()}, status=status.HTTP_200_OK)
    
    except ArtistsModel.DoesNotExist :
        return Response({'msg':'artist not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except MusicModel.DoesNotExist :
        return Response({'msg':'music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
     
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











@api_view(['POST'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_music(request:Request) -> Response:
    """
        - Add music into database by reqeust.data info
        - METHOD : POST
        - Json schema : {'title':Music-name, 'musicfile':Music-file, 'musiccover':Music-musiccover, 'aritst-id':Artist-id, 'lyrics':Music-lyrics, 'duration':Music-duration}
        - Supported image : jpg, png, jpeg
        - Relational with artist models 
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
  
    try:
        
        if  0 <= len(data) < 2 :
            return Response({'msg':'Add values to fields of artist.', 'essential-field':'title, musicfile, musiccover, artist_id', 'optional-fields':'duration, lyrics', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if len(data['title']) == 0 or len(data.getlist('title')) > 1 :
            return Response({'msg':'title is empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)

        if 'musicfile' in data:
            if len(data['musicfile']) == 0 or len(data.getlist('musicfile')) > 1 :
                return Response({'msg':'Only one music is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['musicfile'].name)[-1] not in ['.mp3'] :
                return Response({'msg':'This music type is not supported.', 'supported-musicfile':'mp3', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    
        if 'musiccover' in data: 
            if len(data['musiccover']) == 0 or len(data.getlist('musiccover')) >1 :
                return Response({'msg':'only one music cover is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['musiccover'].name)[-1] not in ['.jpg', '.png', '.jpeg']:
                return Response({'msg':'This music type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if len(data['artist_id']) == 0 or len(data.getlist('artist_id')) < 1 :
            return Response({'msg':'Provide artist\'s id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)

    
            
        artists_id = data.getlist('artist_id')
        artists = ArtistsModel.objects.filter(pk__in=artists_id)
        if artists.count() != len(artists_id):
            return Response({'msg': 'Some artist IDs are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = CreateMusicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Music added, {str(serializer.data)}')
            return Response({'msg':'Music added successfully.', 'status':201, 'data':serializer.data}, status=status.HTTP_201_CREATED)
    
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['PUT'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def update_music(request:Request) -> Response:
    """
        - Update music into database by reqeust.data info
        - METHOD : POST
        - Json schema : {'title':Music-name, 'musicfile':Music-file, 'musiccover':Music-musiccover, 'aritst-id':Artist-id, 'lyrics':Music-lyrics, 'duration':Music-duration}
        - Supported image : jpg, png, jpeg
        - Relational with artist models 
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
        
        if len(data) == 0  or not len(data) > 1 :
            return Response({'msg':'Add this fields to update the music.', 'essential-field':'id', 'optional-fields':'musiccover, duration, lyrics', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data or len(data.getlist('id')) ==0  or len(data.getlist('id')) > 1:
            return Response({'msg':'Provide music pk to update music info.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
    
        if 'musiccover' in data: 
            if len(data['musiccover']) == 0 or len(data.getlist('musiccover')) >1 :
                return Response({'msg':'Only one music cover is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['musiccover'].name)[-1] not in ['.jpg', '.png', '.jpeg']:
                return Response({'msg':'This music type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
    
        music = MusicModel.objects.get(pk=data['id'])
        serializers = UpdateMusicSerializer(music, data=data, partial=True)
        if serializers.is_valid():
            serializers.save()
            logger.info(f'Music info update, {str(serializers.data)} ')
            return Response({'msg':'Music updated successfully.', 'status':200, 'data':serializers.data}, status=status.HTTP_200_OK)
    
    except MusicModel.DoesNotExist:
          return Response({'msg':'The Music does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












@api_view(['DELETE'])
@permission_classes([Is_superadmin])
def delete_music(request:Request) -> Response:
     
    """
        - Delete music from database by reqeust.data info
        - METHOD : DELETE
        - Json schema : {'id':'id'}
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
        if 'id' not in data:
            return Response({'msg':'Music id is required.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' in data and (len(data.getlist('id')) < 1 or len(data['id']) ==0):
            return Response({'msg':'id field is empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        music_pk = data['id']
        music = MusicModel.objects.get(id = music_pk)
        music.artist_id.clear()
        
        if music.musicfile.path:
            musicfile = music.musicfile.path
            os.remove(musicfile)
            
        if music.musiccover.path:
            musiccover = music.musiccover.path
            os.remove(musiccover)
            
        music.delete()
        
        logger.info(f'A music removed , {data["id"]}')
        return Response({'msg':'Music deleted successfully.', 'status':200}, status=status.HTTP_200_OK)
    
    except MusicModel.DoesNotExist :    
        return Response({'msg':'music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
    
    
    
    
    
def download_music(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'musics', filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        return response
    else:
        raise Http404("Music file not found")