from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from urllib.request import Request
from loguru import logger
from typing import Optional
from django.conf import settings
from rest_framework import status
import os 
from os import path



from ..models.albums import AlbumModel 
from ..models.artists import ArtistsModel
from ..models.musics import MusicModel
from ..serializers.albums_serializers import CreateAlbumSerializers, AddArtistToAlbums, RemoveArtistFromAlbums, AddMusicToAlbums, RemoveMusicFromAlbums, UpdateAlbumSerializers, GetAlbumByNameSerializer
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin , Is_superadmin







@api_view(['GET'])
def get_album_by_album_name(request:Response, title:Optional[str]=None) -> Response:
    """
        - Get album data from db 
        - METHOD : Get
        - Json schema : -
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
    
    
    
    
    
    
@api_view(['GET'])
def get_all_albums(request:Request) -> Response:
    """
        - Get album data from db 
        - METHOD : Get
        - Json schema : -
    """
    try:
        paginator = PageNumberPagination()
        pages = {}
        
        allalbums = AlbumModel.objects.all()
        page = paginator.paginate_queryset(allalbums, request)
        serializers = GetAlbumByNameSerializer(instance=page, many=True) 
        
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
         
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link
            
        return Response({'msg':'Albums list.', **pages, 'status':200, 'data':serializers.data, 'total':allalbums.count()}, status=status.HTTP_200_OK)
    except Exception as err :
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   
   














@api_view(['POST'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_album(request:Request) -> Response :
    """
        - Add album into database by reqeust.data info
        - METHOD : POST
        - Json schema :{'title':, 'albumcover':, 'music_id':, 'aritst-id':, 'totaltracks':, 'description':}
        - Supported image : jpg, png, jpeg
        - Relational with artist models and musics
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
        
        if len(data) < 2 :
            return Response({'msg':'Add values to fields of Album.', 'essential-field':'title, albumcover', 'optional-fields':'artist_id, music_id', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'title' not in data or len(data['title']) ==0 or len(data.getlist('title')) < 1 :
                return Response({'msg':'Title length is not enough.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            
        if 'cover' in data:
            if len(data['cover']) == 0 or len(data.getlist('cover')) > 1 :
                return Response({'msg':'album cover must be provided.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['cover'].name)[-1] not in ['.jpg', '.jpeg', '.png']:
                 return Response({'msg':'This file type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
        
        if 'artist_id' in data:
            artist_ids = data.getlist('artist_id')
            
            if not isinstance(artist_ids, list):
                return Response({'msg':'Input value is invalid.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(artist_ids) == 0 or len(data['artist_id']) ==0:
                return Response({'msg': 'Provide valid artist ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                artists = ArtistsModel.objects.filter(pk__in=artist_ids)
                if len(artist_ids) != artists.count():
                    return Response({'msg':'One or more artist ID(s) not found', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
                
                if not artists.exists():
                    return Response({'msg': 'No artist found with provided ID(s).', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        
            
        if 'music_id' in data:
            music_ids = data.getlist('music_id')
            
            if not isinstance(music_ids, list):
                return Response({'msg':'Input value is invalid.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(music_ids) == 0 or len(data['music_id']) ==0:
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
            return Response({'msg':'Album added successfully.', 'status':201, 'data':serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        
    except ArtistsModel.DoesNotExist:    
        return Response({'msg':'Artist does not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)  
    
    except MusicModel.DoesNotExist:
        return Response({'msg':'Music does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







   
   
    
@api_view(['DELETE'])
@permission_classes([Is_superadmin])
def delete_album(request:Request, id:int):
    """
        - Delete album from database by reqeust.data info
        - METHOD : Delete
        - Json schema : {'id':'id'}
        * Only admin's and super-admin's call this endpoint
    """
   
    try:
        if not id :
            return Response({'msg':'Album id is required.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        album = AlbumModel.objects.get(id = id)
        album.artist_id.clear()
        album.music_id.clear()
        
        if album.cover:
            album_coer = album.cover.path
            if path.exists(album_coer):
                os.remove(album_coer)
                
        album.delete()
        
        return Response({'msg':'Album deleted successfully.', 'status':200}, status=status.HTTP_200_OK)
    
    except AlbumModel.DoesNotExist :    
        return Response({'msg':'album not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    






  
@api_view(['PATCH'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_artist_to_Albums(request:Request) -> Response: 
    """
        - Add artist to the Albums
        - METHOD : PATCH
        - Json schema :{id:'', artist_id:''}
        - Relational with artist, musics
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data or 'id' in data and  len(data['id']) < 1 :
            return Response({'msg':'Add id of the albums to add artist.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'artist_id' in data or 'artist_id' in data and len(data['artist_id']) == 0 :
            return Response({'msg':'Provide artist id(s) to add to the albums.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        albums = AlbumModel.objects.get(id= int(data['id']))
        
        serializer = AddArtistToAlbums(albums, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Artist(s) added to albums successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Albums does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
    
    
    
    
    
@api_view(['PATCH'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def remove_artist_from_Albums(request:Request) -> Response: 
    """
        - Remove artist to the Albums
        - METHOD : PATCH
        - Json schema :{id:'', artist_id:''}
        - Relational with artist, musics
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data or 'id' in data and  len(data['id']) < 1 :
            return Response({'msg':'Add id of the albums to remove artist.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'artist_id' in data or 'artist_id' in data and len(data['artist_id']) == 0 :
            return Response({'msg':'Provide artist id(s) to remove from the albums.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        albums = AlbumModel.objects.get(id= int(data['id']))
    
        serializer = RemoveArtistFromAlbums(albums, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Artist(s) removed to albums successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Albums does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    






  
@api_view(['PATCH'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_music_to_Albums(request:Request) -> Response: 
    """
        - Add music to the Albums
        - METHOD : PATCH
        - Json schema :{id:'', music_id:''}
        - Relational with artist, musics
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        print(len(data['id']))
        if not 'id' in data or 'id' in data and  len(data['id']) < 1 :
            return Response({'msg':'Add id of the albums to add music.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'music_id' in data or 'music_id' in data and len(data['music_id']) == 0 :
            return Response({'msg':'Provide music id(s) to add to the albums.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        albums = AlbumModel.objects.get(id= int(data['id']))
        
        serializer = AddMusicToAlbums(albums, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Music(s) added to albums successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Albums does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










    
@api_view(['PATCH'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def remove_music_from_Albums(request:Request) -> Response: 
    """
        - Remove music to the Albums
        - METHOD : PATCH
        - Json schema :{id:'', music_id:''}
        - Relational with artist, musics
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data or 'id' in data and  len(data['id']) < 1 :
            return Response({'msg':'Add id of the albums to remove music.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'music_id' in data or 'music_id' in data and len(data['music_id']) == 0 :
            return Response({'msg':'Provide music id(s) to remove from the albums.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        albums = AlbumModel.objects.get(id= int(data['id']))
    
        serializer = RemoveMusicFromAlbums(albums, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Music(s) removed to albums successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Albums does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





























































@api_view(['PUT'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def update_album(request:Response) -> Response:
    """
        - Add album into database by reqeust.data info
        - METHOD : PUT
        - Json schema :{'title':Album-name, 'albumcover':Album-cover, 'music_id':Music_id, 'aritst-id':Artist-id, 'totaltracks':Album-totaltracks, 'description':Album-description}
        - Supported image : jpg, png, jpeg
        - Relational with artist models and musics
        * Only admin's and super-admin's call this endpoint
    
    """
    data = request.data
    try:
        
        if len(data) == 0 or not len(data) > 1:
            return Response({'msg':'Add values with fields to update the album data.', 'essential-field':'id', 'optional-fields':'title, albumcover, artist_id, music_id, totaltracks,description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data:
            return Response({'msg':'Provide album id to update album data.', 'status':400,}, status=status.HTTP_400_BAD_REQUEST)
        
       
        if 'albumcover' in data:
            if len(data['albumcover']) == 0 or len(data.getlist('albumcover')) > 1:
                return Response({'msg':'Provide image for the albom cover.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
            
            if path.splitext(data['albumcover'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
                return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        if 'artist_id' in data:
            artist_ids = list(data.getlist('artist_id'))
            if  len(artist_ids) == 0 or len(data['artist_id']) == 0:
                return Response({'msg': 'Provide at least one valid artist ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

            artist = ArtistsModel.objects.filter(pk__in = artist_ids)
      
            if  not artist.exists() or artist.count() != len(artist_ids):
                return Response({'msg': 'Some artist IDs are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        if 'music_id' in data:
            music_ids = list(data.getlist('music_id'))
            if len(music_ids) == 0 or len(data['music_id']) == 0 :
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
                
            return Response({'msg':'Album info updated.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
     
        
    except AlbumModel.DoesNotExist:
        return Response({'msg':'Album does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
 
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    







   
   
   
