from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from urllib.request import Request
from loguru import logger
from typing import Optional
from django.conf import settings
from rest_framework import status
import os 
from os import path



from ..models.albums import AlbumModel 
from ..models.artists import ArtistsModels
from ..models.musics import MusicModel
from ..serializers.albums_serializers import CreateAlbumSerializers, UpdateAlbumSerializers, GetAlbumByNameSerializer


@api_view(['POST'])
def add_album(request:Request) -> Response :
    """
        -This function add's album into the database with related artist_id , music_id
        # you can send title/music/artists-id's of the album to save into the database
        #- METHOD : POST
        #- album data scheme : {'title':Album-name, 'albumcover':Album-cover, 'music_id':Music_id, 'aritst-id':Artist-id, 'totaltracks':Album-totaltracks, 'description':Album-description}
        
    """
    data = request.data
    try:
        
        if len(data) < 2 :
            return Response({'msg':'Add this fields to add  music.', 'essential-field':'title, albumcover', 'optional-fields':'artist_id, music_id', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'title' in data:
            if len(data['title']) < 2 :
                return Response({'msg':'Title length is not enough.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            
        if 'albumcover' in data:
            if len(data['albumcover']) == 0 or len(data.getlist('albumcover')) > 1 :
                return Response({'msg':'One album cover must be provided.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['albumcover'].name)[-1] not in ['.jpg', '.jpeg', '.png']:
                 return Response({'msg':'This music type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if 'artist_id' in data:
            artist_ids = data.getlist('artist_id')
            
            if not isinstance(artist_ids, list):
                return Response({'msg':'Input value is invalid.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if all(aid.strip() == '' for aid in artist_ids):
                return Response({'msg': 'Provide at least one valid artist ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                artists = ArtistsModels.objects.filter(pk__in=artist_ids)
                if len(artist_ids) != artists.count():
                    return Response({'msg':'One or more artist ID(s) not found', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
                
                if not artists.exists():
                    return Response({'msg': 'No artist found with provided ID(s).', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        
            
            
            
        if 'music_id' in data:
            music_ids = data.getlist('music_id')
            
            if not isinstance(music_ids, list):
                return Response({'msg':'Input value is invalid.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if all(aid.strip() == '' for aid in music_ids) :
                return Response({'msg': 'Provide at least one valid music ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                musics = MusicModel.objects.filter(pk__in=music_ids)
                if len(music_ids) != musics.count():
                    return Response({'msg':'One or more artist ID(s) not found', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
                
                if not musics.exists():
                    return Response({'msg': 'No music found with provided ID(s).', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
    
        
            
        serializer = CreateAlbumSerializers(data=data)
        if  serializer.is_valid():
            serializer.save()
            return Response({'msg':'Album added successfully.', 'status':201, 'album-ifno':serializer.data}, status=status.HTTP_201_CREATED)
        
        
    
    except ArtistsModels.DoesNotExist:    
        return Response({'msg':'Artist does not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)  
    
    except MusicModel.DoesNotExist:
        return Response({'msg':'Music does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@api_view(['PUT'])
def update_album(request:Response) -> Response:
    """
        -This function update music info into the database
        # you can update title/albumcover/artist_id/music_id/totaltracks/description of the music to save into the database

    """
    data = request.data
    try:
        
        if len(data) == 0 or not len(data) > 1:
            return Response({'msg':'Add this fields to update the album.', 'essential-field':'id', 'optional-fields':'title, albumcover, artist_id, music_id, totaltracks,description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data:
            return Response({'msg':'Provide album pk to update album info.', 'status':400,}, status=status.HTTP_400_BAD_REQUEST)
        
       
        if 'albumcover' in data:
            if len(data['albumcover']) == 0 or len(data.getlist('albumcover')) > 1 :
                return Response({'msg':'Provide one image for the albom cover.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
            
            if path.splitext(data['albumcover'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
                return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        if 'artist_id' in data:
            artist_ids = list(data.getlist('artist_id'))
            if  all(aid.strip() == '' for aid in artist_ids) :
                return Response({'msg': 'Provide at least one valid artist ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

            artist = ArtistsModels.objects.filter(pk__in = artist_ids)
      
            if  not artist.exists() or artist.count() != len(artist_ids):
                return Response({'msg': 'Some artist IDs are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        if 'music_id' in data:
            music_ids = list(data.getlist('music_id'))
            if  all(aid.strip() == '' for aid in music_ids) :
                return Response({'msg': 'Provide at least one valid music ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            
            music = MusicModel.objects.filter(pk__in = music_ids)
            
            if  not music.exists() or music.count() != len(music_ids):
                return Response({'msg': 'Some music IDs are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
             
        album = AlbumModel.objects.get(pk=data['id'])
        serializer = UpdateAlbumSerializers(album, data=data, partial=True)
        
        if serializer.is_valid():
            if 'albumcover' in data:
                image_path = path.join(settings.MEDIA_ROOT, album.albumcover.path)
                if os.path.exists(image_path):
                    os.remove(image_path)
            serializer.save()
            
            if 'artist_id' in data and artist :
                album.artist_id.set(artist)
            if 'music_id' in data and music : 
                album.music_id.set(music)
                
            return Response({'msg':'Album info updated.', 'status':200, 'album':serializer.data}, status=status.HTTP_200_OK)
     
        
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Album does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
 
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    






@api_view(['GET'])
def get_album_by_album_name(request:Response, title:Optional[str]=None) -> Response:
    """
        -This function return's album by name
        #- METHOD : GET
        #- Returns list of albums with fields id, title, albumcover, artist_id, music_id, totaltracks, description
        
    """
    
    try:
        
        info_dict = {}
        
        if title is None :
            return Response({'msg':'Provide album name for searching.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        elif title :
            info_dict['title'] = title 
            
        album = AlbumModel.objects.filter(**info_dict)
        if album:
            serializer = GetAlbumByNameSerializer(instance=album, many=True)
            return Response({'msg':'Album data found successfully.', 'status':200, 'album':serializer.data,}, status=status.HTTP_200_OK)
        
        return Response({'msg':'album not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as err :
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
   
   
    
@api_view(['DELETE'])
def delete_album(request:Request):
    """
        -This function delete Album and all it's info
        #- METHOD : DELETE
            
    """    
    data = request.data
    try:
        if 'id' not in data:
            return Response({'msg':'Album id is required.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' in data and len(data.getlist('id')) <1:
            return Response({'msg':'id field is empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        album_pk = data['id']
        album = AlbumModel.objects.get(id = album_pk)
        album.artist_id.clear()
        album.music_id.clear()
        
        if album.albumcover.path:
            musicfile = album.albumcover.path
            os.remove(musicfile)
        album.delete()
        
        logger.info(f'A album removed / {data["id"]}')
        return Response({'msg':'Album deleted successfully.', 'status':200}, status=status.HTTP_200_OK)
    
    except AlbumModel.DoesNotExist :    
        return Response({'msg':'album not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    