from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from os import path
import os
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.db.models import Q


from ..models.artists import ArtistsModel
from ..models.musics import MusicModel
from ..models.albums import AlbumModel
from ..models.genres import GenereModel
from ..serializers.generes_serializers import CreateGenreSerializers, AddArtistToGenere, RemoveArtistToGenere, AddMusicToGenere, RemoveMusicToGenere, AddAlbumToGenere, RemoveAlbumToGenere,  UpdateGenereSerializers,  GetAllGenereSerializers
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin, Is_superadmin 





  
@api_view(['GET'])
def get_all_genere(request:Request) -> Response:
    """
        - Get genere data from db 
        - METHOD : Get
        - Json schema : -
    """
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
def get_genere(request:Request, qset:int) -> Response:
    """
        - Get genere data from db 
        - METHOD : Get
        - Json schema : -
    """
    try:    

        if not qset:
            return Response({'msg':'Provide genere id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        generes = GenereModel.objects.get(pk = qset)
        serializers = GetAllGenereSerializers(instance=generes)

        
        return Response({'msg':'All the genere.', 'status':200, 'data':serializers.data}, status=status.HTTP_200_OK)
    
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    
      
      
























@api_view(['POST'])      
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_genere(request: Request) -> Response:
    """
        - Add genere into database by reqeust.data info
        - METHOD : POST
        - Json schema :{'name':, 'cover':, 'music_id':, 'aritst-id':, 'album_id':,  'description':}
        - Supported image : jpg, png, jpeg
        - Relational with artist, musics and albums models
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
        
        if len(data) < 1 :
            return Response({'msg':'Add values to fields of genere.', 'essential-field':'name, cover', 'optional-fields':'artist_id, music_idو album_id, description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if 'name' not in data or len(data['name']) ==0 or len(data.getlist('name')) == 0 :
            return Response({'msg':'Provide a name for the genere.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if 'cover' in data:
            if len(data['cover']) == 0 or len(data.getlist('cover')) > 1 :
                return Response({'msg':'One album cover must be provided.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
            if path.splitext(data['cover'].name)[-1] not in ['.jpg', '.jpeg', '.png']:
                 return Response({'msg':'This file type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'artist_id' in data :
            artists_id = data.getlist('artist_id')
            artists = ArtistsModel.objects.filter(pk__in=artists_id)
            if artists.count() != len(artists_id):
                return Response({'msg': 'Some artist ID(s) are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'music_id' in data:     
            musics_id = data.getlist('music_id')
            musics = MusicModel.objects.filter(pk__in=musics_id)
            if musics.count() != len(musics_id):
                return Response({'msg': 'Some music ID(s) are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
             
             
        if 'album_id' in data:     
            albums_id = data.getlist('album_id')
            albums = AlbumModel.objects.filter(pk__in=albums_id)
            if albums.count() != len(albums_id):
                return Response({'msg': 'Some album ID(s) are invalid or missing.', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = CreateGenreSerializers(data=data)        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Genere addedd successfully.', 'status':201, 'data':serializer.data}, status=status.HTTP_201_CREATED)
    
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  
  
  
  
  
  
  


@api_view(['DELETE'])
@permission_classes([Is_superadmin])
def delete_genere(request:Request, id:int) -> Response:
    """
        - Delete genere from database by reqeust.data info
        - METHOD : Delete
        * Only admin's and super-admin's call this endpoint
    """
    try:
        
        if not id:
            return Response({'msg':'Provide genere id.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        genere = GenereModel.objects.get(id=int(id))

        if genere.cover:
            genere_path = genere.cover.path
            if path.exists(genere_path):
                os.remove(genere_path)
            
        
        genere.artist_id.clear()
        genere.music_id.clear()
        genere.album_id.clear()
        
        genere.delete()
        return Response({'msg':'Genere Removed successfully.', 'status':200}, status=status.HTTP_200_OK)
    
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  
  
  
  
  
  
  

  
  
  
  
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_artist_to_genere(request:Request) -> Response: 
    """
        - Add artist to the genere
        - METHOD : PATCH
        - Json schema :{id:'', artist_id:''}
        - Relational with artist, musics and albums models
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data:
            return Response({'msg':'Add id of the genere to add artist.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'artist_id' in data or 'artist_id' in data and len(data['artist_id']) == 0 :
            return Response({'msg':'Provide artist id(s) to add to the genere.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        genere = GenereModel.objects.get(id= int(data['id']))
        
        serializer = AddArtistToGenere(genere, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Artist(s) added to genere successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
        





@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_artist_from_genere(request:Request) -> Response: 
    """
        - Remove artist from the genere
        - METHOD : PATCH
        - Json schema :{id:'', artist_id:''}
        - Relational with artist, musics and albums models
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data:
            return Response({'msg':'Add id of the genere to add artist.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'artist_id' in data or 'artist_id' in data and len(data['artist_id']) == 0 :
            return Response({'msg':'Provide artist id(s) to add to the genere.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        genere = GenereModel.objects.get(id= int(data['id']))
        
        serializer = RemoveArtistToGenere(genere, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Artist(s) removed from genere successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
        


  
  
  
  
  
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_music_to_genere(request:Request) -> Response: 
    """
        - Add music to the genere
        - METHOD : PATCH
        - Json schema :{id:'', music_id:''}
        - Relational with artist, musics and albums models
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data:
            return Response({'msg':'Add id of the genere to add artist.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'music_id' in data or 'music_id' in data and len(data['music_id']) == 0 :
            return Response({'msg':'Provide music id(s) to add to the genere.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        genere = GenereModel.objects.get(id= int(data['id']))
        
        serializer = AddMusicToGenere(genere, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Music(s) added to genere successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
        



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_music_from_genere(request:Request) -> Response: 
    """
        - Remove music from the genere
        - METHOD : PATCH
        - Json schema :{id:'', music_id:''}
        - Relational with artist, musics and albums models
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data:
            return Response({'msg':'Add id of the genere to add music.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'music_id' in data or 'music_id' in data and len(data['music_id']) == 0 :
            return Response({'msg':'Provide music id(s) to add to the genere.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        genere = GenereModel.objects.get(id= int(data['id']))
        
        serializer = RemoveMusicToGenere(genere, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Music(s) removed from genere successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


  
  
  

  
  

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_album_to_genere(request:Request) -> Response: 
    """
        - Add album to the genere
        - METHOD : PATCH
        - Json schema :{id:'', album_id:''}
        - Relational with artist, musics and albums models
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data:
            return Response({'msg':'Add id of the genere to add album.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'album_id' in data or 'album_id' in data and len(data['album_id']) == 0 :
            return Response({'msg':'Provide album id(s) to add to the genere.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        genere = GenereModel.objects.get(id= int(data['id']))
        
        serializer = AddAlbumToGenere(genere, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Album(s) added to genere successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
        



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_album_from_genere(request:Request) -> Response: 
    """
        - Remove album from the genere
        - METHOD : PATCH
        - Json schema :{id:'', album_id:''}
        - Relational with artist, musics and albums models
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    
    try:
        
        if not 'id' in data:
            return Response({'msg':'Add id of the genere to add album.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'album_id' in data or 'album_id' in data and len(data['album_id']) == 0 :
            return Response({'msg':'Provide music id(s) to add to the genere.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
       
       
        genere = GenereModel.objects.get(id= int(data['id']))
        
        serializer = RemoveAlbumToGenere(genere, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Album(s) removed from genere successfully.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'msg':'An error occured.', 'status':400, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exists.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


  
  
  
  
  
  

@api_view(['PUT'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def update_genere(request:Response) -> Response:
    """
        - Add genere into database by reqeust.data info
        - METHOD : PUT
        - Json schema :{'name':, 'cover':,  'description':}
        - Supported image : jpg, png, jpeg
        - Relational with artist, musics and albums models
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
        
        if len(data) == 0 or not len(data) > 1:
            return Response({'msg':'Add values with fields to update the genere data.', 'essential-field':'id', 'optional-fields':'title, cover, description', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data:
            return Response({'msg':'Provide genere id to update genere data.', 'status':400,}, status=status.HTTP_400_BAD_REQUEST)
        
       
        if 'cover' in data:
            if len(data['cover']) == 0 or len(data.getlist('cover')) > 1:
                return Response({'msg':'Provide image for the albom cover.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
            
            if path.splitext(data['cover'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
                return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        
   
        genere = GenereModel.objects.get(pk=data['id'])
        serializer = UpdateGenereSerializers(genere, data=data, partial=True)
        
        if serializer.is_valid():
            if 'cover' in data:
                if genere.cover : 
                    image_path = path.join(settings.MEDIA_ROOT, genere.cover.path)
                    if os.path.exists(image_path):
                        os.remove(image_path)
            serializer.save()
            
            return Response({'msg':'Genere info updated.', 'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
     
        
    except GenereModel.DoesNotExist:
        return Response({'msg':'Genere does not exits', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
 
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


