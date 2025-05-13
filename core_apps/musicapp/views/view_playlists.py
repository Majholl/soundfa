from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.conf import settings
from os import path
import os



from ..serializers.playlists_serializers import CreatePlayListSerializers, AddMusicToPlaylist, RemoveMusicToPlaylist,  UpdatePlayListSerializers, GetAllListsSerializers, GetAllPublicListsSerializers
from ..models.albums import AlbumModel 
from ..models.musics import MusicModel
from ..models.playlists import PlaylistModel
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin , Is_superadmin




User = get_user_model()





@api_view(['GET'])
def get_all_public_playlist(request:Request) -> Response:
    """
        - Get all public playlists data from db 
        - METHOD : Get
        - Json schema : -
    """    
    try:    
        paginator = PageNumberPagination()
        pages = {}
        
        playlists = PlaylistModel.objects.filter(public_playlist= 1).all()
        page = paginator.paginate_queryset(playlists, request)
        serializers = GetAllPublicListsSerializers(instance=page, many=True, context={'request':request})
        
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
        
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link
            
        return Response({'msg':'All the public playlists.', **pages, 'total': playlists.count(), 'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_playlist_user(request:Request) -> Response:
    """
        - Get all user playlists data from db 
        - METHOD : Get
        - Json schema : -
    """
    user = request.user
    try:    
        paginator = PageNumberPagination()
        pages = {}
        
        playlist_id = user.playlists.values_list('id', flat=True)
        playlists = PlaylistModel.objects.filter(pk__in=playlist_id).all()
        page = paginator.paginate_queryset(playlists, request)
        serializers = GetAllListsSerializers(instance=page, many=True, context={'request':request})
        
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
        
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link
            
        return Response({'msg':'All the playlists.', **pages, 'total': playlists.count(),'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    
    
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_playlist_user(request:Request) -> Response:
    data = request.data
    user = request.user
    try:    
        if not 'playlist_id' in data:
            return Response({'msg':'Provide Playlist id for the user.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        playlists = PlaylistModel.objects.get(pk=data['playlist_id'])
        
        if str(playlists.playlists_users.values('id')[0]['id']) != str(user.pk)  and user.usertype not in ['admin', 'superadmin']:
            return Response({'msg':"You are not owner of this playlisy", 'status':403}, status=status.HTTP_403_FORBIDDEN)

        serializers = GetAllListsSerializers(instance=playlists, context={'request':request})
        return Response({'msg':'All the playlists.', 'status':200, 'playlist':serializers.data}, status=status.HTTP_200_OK)
    
    except PlaylistModel.DoesNotExist:
        return Response({'msg':'Playlist does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    
    
    
    
     













@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_playlist(request:Response) -> Response:
    """
        - Add playlist into database by reqeust.data info
        - METHOD : POST
        - Json schema :{title:'', cover:'', music_id:'', public_playlist:'', totaltracks:'', description:''}
        - Supported image : jpg, png, jpeg
        - Relational with musics models
        * Only users who is owner of the playlist or admins and superadmins can call this endpoints
    """
    data = request.data
    
    try:
        
        if len(data) == 0 or not len(data) > 0:
            return Response({'msg':'Add this fields to add a album.', 'essential-field':'title', 'optional-fields':'cover, music_id, description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'title' not in data or len(data['title']) ==0 or len(data.getlist('title')) < 1 :
                return Response({'msg':'Title length is not enough.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            
        if 'music_id' in data:
            music_ids = data.getlist('music_id')
            
            if not isinstance(music_ids, list):
                return Response({'msg':'Input value is invalid.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(music_ids) == 0 or len(data['music_id']) ==0:
                return Response({'msg': 'Provide at least one valid music ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                musics = MusicModel.objects.filter(pk__in=music_ids)
                if len(music_ids) != musics.count():
                    return Response({'msg':'One or more music ID(s) not found', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
                
                if not musics.exists():
                    return Response({'msg': 'No music found with provided ID(s).', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
    
        if 'cover' in data:
            if len(data['cover']) == 0 or len(data.getlist('cover')) > 1 :
                return Response({'msg':'One cover for playlist must be provided.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['cover'].name)[-1] not in ['.jpg', '.jpeg', '.png']:
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















@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_playlist(request:Request, id:int) -> Response:
    """
        - Delete playlist from database by id 
        - METHOD : DELETE
        - Relational with musics and users models
        * Only users who is owner of the playlist or admins and superadmins can call this endpoints
    """
    user = request.user
    try:
        
        if not id:
            return Response({'msg':'Provide playlist id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        playlist = PlaylistModel.objects.get(id= int(id))
        
        if str(playlist.playlists_users.values('id')[0]['id']) != str(user.pk)  and user.usertype not in ['admin', 'superadmin']:
            return Response({'msg':"You are not owner of this playlist", 'status':403}, status=status.HTTP_403_FORBIDDEN)

        playlist.music_id.clear()
        user.playlists.remove(playlist)
        
        if playlist.cover.path:
            os.remove(playlist.cover.path)
        
        playlist.delete()
        return Response({'msg':'playlist Removed successfully.', 'status':201}, status=status.HTTP_201_CREATED)
    
    except PlaylistModel.DoesNotExist:
        return Response({'msg':'Playlist does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_music_to_playlist(request:Request) -> Response: 
    """
        - Add music to the playlist
        - METHOD : PATCH
        - Json schema :{id:'', music_id:''}
        - Relational with musics models
        * Only users who is owner of the playlist or admins and superadmins can call this endpoints
    """
    data = request.data
    
    try:
        if not 'id' in data:
            return Response({'msg':'Add id of the playlist to add music.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        if not 'music_id' in data or 'music_id' in data and len(data['music_id']) == 0 :
            return Response({'msg':'Provide music id(s) to add to the playlist.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
        playlist = PlaylistModel.objects.get(id= int(data['id']))
        serializer = AddMusicToPlaylist(playlist, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Music(s) added to playlists.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except PlaylistModel.DoesNotExist:
        return Response({'msg':'Playlist does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
        


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_music_to_playlist(request:Request) -> Response: 
    """
        - Remove music to the playlist
        - METHOD : PATCH
        - Json schema :{id:'', music_id:''}
        - Relational with musics models
        * Only users who is owner of the playlist or admins and superadmins can call this endpoints
    """
    data = request.data
    
    try:
        if not 'id' in data:
            return Response({'msg':'Add id of the playlist to add music.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'music_id' in data or 'music_id' in data and len(data['music_id']) == 0 :
            return Response({'msg':'Provide music id(s) to add to the playlist.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
        playlist = PlaylistModel.objects.get(id= int(data['id']))
        serializer = RemoveMusicToPlaylist(playlist, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Music(s) added to playlists.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except PlaylistModel.DoesNotExist:
        return Response({'msg':'Playlist does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
















@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_playlist(request:Response) -> Response:
    """
        - Update playlist into database by reqeust.data info
        - METHOD : POST
        - Json schema :{title:'', cover:'', music_id:'', public_playlist:'', totaltracks:'', description:''}
        - Supported image : jpg, png, jpeg
        - Relational with musics models
        * Only users who has the  playlist and superadmins and admins can call this 
    """
    data = request.data
    user = request.user
    try:
        
        if len(data) == 0 or not len(data) > 1:
            return Response({'msg':'Add this fields to update the playlist.', 'essential-field':'id', 'optional-fields':'title, playlistcover, music_id, totaltracks,description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data or len(data.getlist('id')) ==0  or len(data.getlist('id')) > 1:
            return Response({'msg':'Provide playlist pk to update playlist info.', 'status':400,}, status=status.HTTP_400_BAD_REQUEST)
        
       
        if 'cover' in data:
            if len(data['musiccover']) == 0 or len(data.getlist('musiccover')) >1 :
                return Response({'msg':'Provide a cover for the playlsit.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
            
            if path.splitext(data['cover'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
                return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if 'music_id' in data:
            
            music_ids = list(data.getlist('music_id'))
            
            if  len(music_ids) == 0 or len(data['music_id']) == 0:
                return Response({'msg': 'Provide at least one valid music ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            
            music = MusicModel.objects.filter(pk__in = music_ids)
            
            if  not music.exists() or music.count() != len(music_ids):
                return Response({'msg': 'Some music IDs are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
             
             
        playlist = PlaylistModel.objects.get(pk=data['id'])
        
        if str(playlist.playlists_users.values('id')[0]['id']) != str(user.pk)  and user.usertype not in ['admin', 'superadmin']:
            return Response({'msg':"You are not owner of this playlisy", 'status':403}, status=status.HTTP_403_FORBIDDEN)

        serializer = UpdatePlayListSerializers(playlist, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            if 'playlistcover' in data:
                image_path = path.join(settings.MEDIA_ROOT, playlist.playlistcover.path)
                if os.path.exists(image_path):
                    os.remove(image_path)
            serializer.save()
            
            if 'music_id' in data and music : 
                for i in music:
                    playlist.music_id.add(i)
                
            return Response({'msg':'Playlist info updated.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
     
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
                
    except PlaylistModel.DoesNotExist:
        return Response({'msg':'Playlist does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
              
              
    except MusicModel.DoesNotExist:
        return Response({'msg':'Music does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
      
 
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
