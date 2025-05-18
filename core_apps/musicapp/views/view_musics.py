from rest_framework.decorators import api_view, permission_classes
from urllib.request import Request
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import FileResponse, Http404
from django.conf import settings
from django.db.models import Q
from loguru import logger
from typing import Optional
from os import path
import os


from ..models.artists import ArtistsModel
from ..models.musics import MusicModel
from ..serializers.musics_serializers import CreateMusicSerializer, UpdateMusicSerializer , GetMusicByNameSerializer
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin , Is_superadmin






@api_view(['GET'])
def search_in_musics_artists(request:Request) -> Response:
    """
        - Get music & artist data from db 
        - METHOD : Get
        - Json schema : -
    """
    param = request.query_params.get('search')
    try:
        paginator = PageNumberPagination()
        if not param:
            return Response({'msg':'Data found.', 'stats':200, 'data':''}, status=status.HTTP_200_OK)
         
        pages  = {}
        
        music = MusicModel.objects.filter(Q(title__icontains = param) | Q(artist_id__name__icontains = param)).distinct()
        page = paginator.paginate_queryset(music, request)    
          
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
        
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link
             
        serializer = GetMusicByNameSerializer(instance=page , many=True, context={'request':request})
        return Response({'msg':'Music data found successfully.', **pages,  'status':200, 'data':serializer.data, 'total':music.count()}, status=status.HTTP_200_OK)
    
    
    except ArtistsModel.DoesNotExist :
        return Response({'msg':'Artist not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except MusicModel.DoesNotExist :
        return Response({'msg':'Music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
         
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@api_view(['GET'])
def get_music_by_musicname(request:Request, qset:Optional[str]=None) -> Response:
    """
        - Get music data by it's name from db 
        - METHOD : Get
        - Json schema : -
    """
    try:
        paginator = PageNumberPagination()
        pages  = {}
        if qset is None:
            return Response({'msg':'Need music title to search for.', 'stats':400}, status=status.HTTP_400_BAD_REQUEST)
                 
        music = MusicModel.objects.filter(Q(title__icontains = qset)).distinct()
        
        if music.count() == 0 :
            return Response({'msg':'Data found.', 'stats':200, 'data':''}, status=status.HTTP_200_OK)
        
        page = paginator.paginate_queryset(music, request)    
          
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
        
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link
        
        serializer = GetMusicByNameSerializer(instance=page , many=True, context={'request':request})
        return Response({'msg':'Music data found successfully.', 'status':200, 'data':serializer.data, 'total':music.count()}, status=status.HTTP_200_OK)
    
    except ArtistsModel.DoesNotExist :
        return Response({'msg':'Artist not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except MusicModel.DoesNotExist :
        return Response({'msg':'Music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
         
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['GET'])
def get_music_by_artistname(request:Request, qset:Optional[str]=None) -> Response:
    """
        - Get music data by it's artist from db 
        - METHOD : Get
        - Json schema : -
    """
    try:
        paginator = PageNumberPagination()
        pages  = {}
        if qset is None:
            return Response({'msg':'Need music title to search for.', 'stats':400}, status=status.HTTP_400_BAD_REQUEST)
                 
              
        music = MusicModel.objects.filter(Q(artist_id__name__icontains= qset)).distinct()
        if music.count() == 0 :
            return Response({'msg':'Data found.', 'stats':200, 'data':''}, status=status.HTTP_200_OK)
        
        page = paginator.paginate_queryset(music, request)    
          
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
        
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link
        
        serializer = GetMusicByNameSerializer(instance=page , many=True, context={'request':request})
        return Response({'msg':'Music data found successfully.', **pages,  'status':200, 'data':serializer.data, 'total':music.count()}, status=status.HTTP_200_OK)
    
    except ArtistsModel.DoesNotExist :
        return Response({'msg':'Artist not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except MusicModel.DoesNotExist :
        return Response({'msg':'Music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
     
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@api_view(['GET'])
def get_all_musics(request:Request) -> Response:
    """
        - Get all musics from db
        - METHOD : Get
        - Json schema : -
    """
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 10
        pages = {}
        musics = MusicModel.objects.all()
        page = paginator.paginate_queryset(musics, request)
        serializer = GetMusicByNameSerializer(instance=page, many=True, context={'request':request})
        
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
        
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link
            
        return Response({'msg':'Music data found successfully.', **pages,  'status':200, 'data':serializer.data, 'total':musics.count()}, status=status.HTTP_200_OK)
    
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











@api_view(['POST'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_music(request:Request) -> Response:
    """
        - Add music into database by reqeust.data info
        - METHOD : POST
        - Json schema : {'title':, 'file':file, 'cover':, 'aritst-id':, 'lyrics':, 'duration':}
        - Supported image : jpg, png, jpeg
        - Relational with artist models 
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
  
    try:
        
        if  0 <= len(data) < 2 :
            return Response({'msg':'Add values to fields of artist.', 'essential-field':'title, file, cover, artist_id', 'optional-fields':'duration, lyrics', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if len(data['title']) == 0 or len(data.getlist('title')) > 1 :
            return Response({'msg':'title is empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)

        if 'file' in data:
            if len(data['file']) == 0 or len(data.getlist('file')) > 1 :
                return Response({'msg':'Only one music is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['file'].name)[-1] not in ['.mp3'] :
                return Response({'msg':'This file type is not supported.', 'supported-musicfile':'mp3', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    
        if 'cover' in data: 
            if len(data['cover']) == 0 or len(data.getlist('cover')) >1 :
                return Response({'msg':'only one music cover is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['cover'].name)[-1] not in ['.jpg', '.png', '.jpeg']:
                return Response({'msg':'This file type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if len(data['artist_id']) == 0 or len(data.getlist('artist_id')) < 1 :
            return Response({'msg':'Provide artist(s) id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)

    
            
        artists_id = data.getlist('artist_id')
        artists = ArtistsModel.objects.filter(pk__in=artists_id)
        if artists.count() != len(artists_id):
            return Response({'msg': 'Some artist ID(s) are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

        
        
        serializer = CreateMusicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Music added, {str(serializer.data)}')
            return Response({'msg':'Music added successfully.', 'status':201, 'data':serializer.data}, status=status.HTTP_201_CREATED)
    
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









@api_view(['DELETE'])
@permission_classes([Is_superadmin])
def delete_music(request:Request, id:int) -> Response:
     
    """
        - Delete music from database by id
        - METHOD : DELETE
        * Only admin's and super-admin's call this endpoint
    """
    try:
        if not id :
            return Response({'msg':'Music id is required.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
         
        music = MusicModel.objects.get(id = int(id))
        music.artist_id.clear()
        
        if music.file:
            musicfile = music.file.path
            if os.path.exists(musicfile):
                os.remove(musicfile)
            
        if music.cover:
            musiccover = music.cover.path
            if os.path.exists(musiccover):
                os.remove(musiccover)
            
        music.delete()
        
        return Response({'msg':'Music deleted successfully.', 'status':200}, status=status.HTTP_200_OK)
    
    except MusicModel.DoesNotExist :    
        return Response({'msg':'music not found.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
    
    
    




@api_view(['PUT'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def update_music(request:Request) -> Response:
    """
        - Update music into database by reqeust.data info
        - METHOD : POST
        - Json schema : {'title':, 'file':, 'cover':, 'aritst-id':, 'lyrics':, 'duration':}
        - Supported image : jpg, png, jpeg
        - Relational with artist models 
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
        
        if len(data) == 0  or not len(data) > 1 :
            return Response({'msg':'Add this fields to update the music.', 'essential-field':'id', 'optional-fields':'cover, duration, lyrics', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data or len(data.getlist('id')) ==0  or len(data.getlist('id')) > 1:
            return Response({'msg':'Provide music pk to update music info.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
    
        if 'cover' in data: 
            if len(data['cover']) == 0 or len(data.getlist('cover')) >1 :
                return Response({'msg':'Only one music cover is allowed.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['cover'].name)[-1] not in ['.jpg', '.png', '.jpeg']:
                return Response({'msg':'This music type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
    
        music = MusicModel.objects.get(pk=data['id'])
        serializer = UpdateMusicSerializer(music, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Music updated successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    except MusicModel.DoesNotExist:
          return Response({'msg':'The Music does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












    
    
    
    
    
    
    
def download_music(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'musics', filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        return response
    else:
        raise Http404("Music file not found")