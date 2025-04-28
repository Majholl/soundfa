from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from os import path
import os
from rest_framework.pagination import PageNumberPagination
from django.conf import settings

from ..models.artists import ArtistsModel
from ..models.musics import MusicModel
from ..models.albums import AlbumModel
from ..models.genres import GenereModel
from ..serializers.generes_serializers import CreateGenreSerializers, UpdateGenereSerializers,  GetAllGenereSerializers
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin, Is_superadmin 





  
@api_view(['GET'])
def get_all_genere(request) -> Response:
    """
        - Get genere data from db 
        - METHOD : Get
        - Json schema : -
    """
    data = request.data
    try:    
        paginator = PageNumberPagination()
        pages = {}
        
        
        playlists = GenereModel.objects.all()
        page = paginator.paginate_queryset(playlists, request)
        
        serializers = GetAllGenereSerializers(instance=page, many=True)
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
         
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link

        return Response({'msg':'All the generes.', **pages, 'status':200, 'data':serializers.data}, status=status.HTTP_200_OK)
    
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    
    
    
    
    
@api_view(['GET'])
def get_genere(request) -> Response:
    """
        - Get genere data from db 
        - METHOD : Get
        - Json schema : -
    """
    data = request.data
    try:    
        if not 'genere_id' in data:
            return Response({'msg':'Provide genere id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        playlists = GenereModel.objects.get(pk=data['genere_id'])
        
        serializers = GetAllGenereSerializers(instance=playlists)
        return Response({'msg':'All the genere.', 'status':200, 'data':serializers.data}, status=status.HTTP_200_OK)
    
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
      
      
      






@api_view(['POST'])      
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_genere(request)  -> Response:
    """
        - Add genere into database by reqeust.data info
        - METHOD : POST
        - Json schema :{'title':genere-name, 'generecover':genere-cover, 'music_id':Music_id, 'aritst-id':Artist-id, 'description':genere-description}
        - Supported image : jpg, png, jpeg
        - Relational with artist models and musics
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
        
        if len(data) < 1 :
            return Response({'msg':'Add values to fields of genere.', 'essential-field':'name, generecover', 'optional-fields':'artist_id, music_idو album_id, description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'name' not in data or len(data['name']) ==0 or len(data.getlist('name')) == 0 :
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
  
  
  
  
  
  
  


@api_view(['PUT'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def update_genere(request:Response) -> Response:
    """
        - Add genere into database by reqeust.data info
        - METHOD : PUT
        - Json schema :{'title':genere-name, 'generecover':genere-cover, 'music_id':Music_id, 'aritst-id':Artist-id, 'description':genere-description}
        - Supported image : jpg, png, jpeg
        - Relational with artist models and musics
        * Only admin's and super-admin's call this endpoint
    
    """
    data = request.data
    try:
        
        if len(data) == 0 or not len(data) > 1:
            return Response({'msg':'Add values with fields to update the genere data.', 'essential-field':'id', 'optional-fields':'title, generecover, artist_id, music_id, description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data:
            return Response({'msg':'Provide genere id to update genere data.', 'status':400,}, status=status.HTTP_400_BAD_REQUEST)
        
       
        if 'generecover' in data:
            if len(data['generecover']) == 0 or len(data.getlist('generecover')) > 1:
                return Response({'msg':'Provide image for the albom cover.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
            
            if path.splitext(data['generecover'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
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



        if 'album_id' in data:
            album_ids = list(data.getlist('album_id'))
            if len(album_ids) == 0 or len(data['album_id']) == 0 :
                return Response({'msg': 'Provide at least one valid album ID.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            
            album = AlbumModel.objects.filter(pk__in = album_ids)
            
            if  not album.exists() or album.count() != len(album_ids):
                return Response({'msg': 'Some album IDs are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
   
        
   
        genere = GenereModel.objects.get(pk=data['id'])
        serializer = UpdateGenereSerializers(genere, data=data, partial=True)
        
        if serializer.is_valid():
            if 'generecover' in data:
                image_path = path.join(settings.MEDIA_ROOT, genere.generecover.path)
                if os.path.exists(image_path):
                    os.remove(image_path)
            serializer.save()
            
            if 'artist_id' in data and artist :
                genere.artist_id.set(artist)
                
            if 'music_id' in data and music : 
                genere.music_id.set(music)
                
            if 'album_id' in data and album:
                print(album)
                genere.album_id.set(album)
                
            return Response({'msg':'Genere info updated.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
     
        
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
 
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    





@api_view(['DELETE'])
@permission_classes([Is_superadmin])
def delete_genere(request) -> Response:
    """
        - Delete genere from database by reqeust.data info
        - METHOD : Delete
        - Json schema : {'id':'id'}
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'genere_id' in data or len(data)== 0 or len(data.getlist('id')) <1:
            return Response({'msg':'Provide genere id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        genere = GenereModel.objects.get(id=data['genere_id'])
        if genere.generecover.path:
            generes = genere.generecover.path
            os.remove(generes)
            
        genere.artist_id.clear()
        genere.music_id.clear()
        genere.album_id.clear()
        
        genere.delete()
        return Response({'msg':'Genere Removed successfully.', 'status':201}, status=status.HTTP_201_CREATED)
    
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
