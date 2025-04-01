from math import inf
from tkinter import EXCEPTION
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from loguru import logger
from os import path
import os
from ..models.artists import ArtistsModels
from ..models.musics import MusicModel
from ..serializers.musics_serializers import CreateMusicSerializer, UpdateMusicSerializer , GetMusicByNameSerializer
from typing import Optional







@api_view(['POST'])
def add_music(request) -> Response:
    """
        -This function add's music into the database
        ## you can send title/music/artists-id's of the music to save into the database
    """
    data = request.data
  
    try:
        artists_id = data.getlist('artist_id')   
        
        if len(artists_id) <1 :
            return Response({'msg':'at least Provide one artist id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if 'musicfile' in data:
            if len(data.getlist('musicfile')) >1 :
                return Response({'msg':'Only one music is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['musicfile'].name)[-1] not in ['.mp3'] :
                return Response({'msg':'This music type is not supported.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
        
        if 'musiccover' in data: 
            if len(data.getlist('musiccover')) >1:
                return Response({'msg':'only one music cover is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['musiccover'].name)[-1] not in ['.jpg', '.png', '.jpeg']:
                return Response({'msg':'This music type is not supported.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            

        serializer = CreateMusicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'A music added / {str(serializer.data)}')
            return Response({'msg':'Music added successfully.', 'status':200, 'music':serializer.data}, status=status.HTTP_200_OK)
    
    except ArtistsModels.DoesNotExist:
        return Response({'msg':'Artist not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)    
        
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











@api_view(['PUT'])
def update_music(request) -> Response:
    """
        -This function update music info into the database
        ## you can update duration/lyrics/musiccover of the music to save into the database
    """
    data = request.data
    try:
        
        music = MusicModel.objects.get(pk=data['id'])
        
        serializers = UpdateMusicSerializer(music, data=data, partial=True)
        if serializers.is_valid():
            serializers.save()
        logger.info(f'Music data updated to / {str(serializers.data)} ')

        return Response({'msg':'Music updated successfully.', 'status':200, 'music':serializers.data}, status=status.HTTP_200_OK)
    
    except MusicModel.DoesNotExist:
          return Response({'msg':'The Music does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
        
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['GET'])
def get_music_by_musicname(request, name:Optional[str]=None) -> Response:
    """
        -This function return's music by name'
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
            return Response({'msg':'Musci not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GetMusicByNameSerializer(instance=music , many=True)
        return Response({'msg':'Music data found successfully.', 'status':200, 'music':serializer.data}, status=status.HTTP_200_OK)
    
    
    except ArtistsModels.DoesNotExist :
        return Response({'msg':'artist not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except MusicModel.DoesNotExist :
        return Response({'msg':'music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
         
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














@api_view(['GET'])
def get_music_by_artistname(request, name:Optional[str]=None) -> Response:
    """
        -This function return's music by artist name '
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
            
        artist = ArtistsModels.objects.get(**info_dict)
        music = MusicModel.objects.filter(artist_id = artist.pk)
        if music.count() == 0 :
            return Response({'msg':'Musci not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GetMusicByNameSerializer(instance=music , many=True)
        return Response({'msg':'Music data found successfully.', 'status':200, 'music':serializer.data}, status=status.HTTP_200_OK)
    
    except ArtistsModels.DoesNotExist :
        return Response({'msg':'artist not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except MusicModel.DoesNotExist :
        return Response({'msg':'music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
     
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['DELETE'])
def delete_music(request):
    data = request.data
    try:
        if 'id' not in data:
            return Response({'msg':'Music id is required.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' in data and len(data.getlist('id')) <1:
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
        
        logger.info(f'A music removed / {data['id']}')
        return Response({'msg':'Music deleted successfully.', 'status':200}, status=status.HTTP_200_OK)
    
    except MusicModel.DoesNotExist :    
        return Response({'msg':'music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except EXCEPTION as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)