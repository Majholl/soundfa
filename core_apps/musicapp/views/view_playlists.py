from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from os import path
import os
from django.conf import settings

from ..serializers.playlists_serializers import CreatePlayListSerializers, UpdatePlayListSerializers, GetAllListsSerializers
from ..models.albums import AlbumModel 
from ..models.musics import MusicModel
from ..models.playlists import PlaylistModel
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin , Is_superadmin


User = get_user_model()




@api_view(['POST'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_playlist(request:Response) -> Response:
    data = request.data
    
    try:
        if len(data) == 0 or not len(data) > 1:
            return Response({'msg':'Add this fields to update the album.', 'essential-field':'id', 'optional-fields':'title, albumcover, artist_id, music_id, totaltracks,description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'title' not in data  or 'title' in data and all(title.strip()=='' for title in data['title']):
            return Response({'msg':'Provide a title for the playlist.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)

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
    
        if 'playlistcover' not in data:
            return Response({'msg':'Provide a cover for the playlsit.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'playlistcover' in data:
            if len(data['playlistcover']) == 0 or len(data.getlist('playlistcover')) > 1 :
                return Response({'msg':'One cover for playlist must be provided.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['playlistcover'].name)[-1] not in ['.jpg', '.jpeg', '.png']:
                 return Response({'msg':'This music type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
        
        serializer = CreatePlayListSerializers(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Playlist added successfully.', 'status':201, 'data':serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except MusicModel.DoesNotExist:
        return Response({'msg':'Music does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
      
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











@api_view(['PUT'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def update_playlist(request:Response) -> Response:

    data = request.data
    try:
        
        if len(data) == 0 or not len(data) > 1:
            return Response({'msg':'Add this fields to update the playlist.', 'essential-field':'id', 'optional-fields':'title, playlistcover, music_id, totaltracks,description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data or 'id' in data and all(title.strip()=='' for title in data['id']):
            return Response({'msg':'Provide playlist pk to update playlist info.', 'status':400,}, status=status.HTTP_400_BAD_REQUEST)
        
       
        if 'playlistcover' in data:
            if len(data['playlistcover']) == 0 or 'playlistcover' in data and all(title.strip()=='' for title in data['playlistcover']) :
                return Response({'msg':'Provide a cover for the playlsit.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
            
            if path.splitext(data['playlistcover'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
                return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if 'music_id' in data:
            music_ids = list(data.getlist('music_id'))
            if  all(aid.strip() == '' for aid in music_ids) :
                return Response({'msg': 'Provide at least one valid music ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            music = MusicModel.objects.filter(pk__in = music_ids)
            if  not music.exists() or music.count() != len(music_ids):
                return Response({'msg': 'Some music IDs are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
             
             
        playlist = PlaylistModel.objects.get(pk=data['id'])
        serializer = UpdatePlayListSerializers(playlist, data=data, partial=True)
        
        if serializer.is_valid():
            if 'playlistcover' in data:
                image_path = path.join(settings.MEDIA_ROOT, playlist.playlistcover.path)
                if os.path.exists(image_path):
                    os.remove(image_path)
            serializer.save()
            
            if 'music_id' in data and music : 
                playlist.music_id.set(music)
                
            return Response({'msg':'Playlist info updated.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
     
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
        
    except MusicModel.DoesNotExist:
        return Response({'msg':'Music does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
      
 
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


















@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_playlist_user(request):
    user = request.user
    try:    
        playlist_id = user.playlists.values_list('id', flat=True)
        playlists = PlaylistModel.objects.filter(pk__in=playlist_id).all()
        serializers = GetAllListsSerializers(instance=playlists, many=True)
        return Response({'msg':'All the playlists.', 'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    
    
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_playlist_user(request):
    data = request.data
    try:    
        if not 'playlist_id' in data:
            return Response({'msg':'Provide Playlist id for the user.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        playlists = PlaylistModel.objects.get(pk=data['playlist_id'])
        
        serializers = GetAllListsSerializers(instance=playlists)
        return Response({'msg':'All the playlists.', 'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except PlaylistModel.DoesNotExist:
        return Response({'msg':'Playlist does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    
    
    
    
    
    

@api_view(['DELETE'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def delete_playlist(request):
    data = request.data
    user = request.user
    try:
        
        if not 'playlist_id' in data:
            return Response({'msg':'Provide playlist id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        album = PlaylistModel.objects.get(id=data['playlist_id'])
        print(album)
        album.music_id.clear()
        user.playlists.remove(album)
        album.delete()
        return Response({'msg':'playlist Removed successfully.', 'status':201}, status=status.HTTP_201_CREATED)
    
    except PlaylistModel.DoesNotExist:
        return Response({'msg':'Playlist does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
