from urllib.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import  PageNumberPagination
from rest_framework import status
from loguru import logger
from django.db.models import Q
from django.conf import settings
from os import path
import os
from typing import Optional



from ..serializers.artists_serializers import CreateArtistsSerialiazer, UpdateDataArtistSerializer, GetArtitstsSerialiazer
from ..models.artists import ArtistsModel
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin , Is_superadmin





@api_view(['GET'])
def get_all_artists(request:Request) -> Response:
    """
        - Get artist data from db 
        - METHOD : Get
        - Json schema : -
    """
    try :
        paginator = PageNumberPagination()
        
        params = request.query_params
        pages = {}
        
        default_order = '-name'
        if 'order' in params :
            default_order = params['order']
            
        allArtists = ArtistsModel.objects.all().order_by((default_order))
        page = paginator.paginate_queryset(allArtists, request)
        serializers = GetArtitstsSerialiazer(page , many=True)
        
        next_link = paginator.get_next_link() 
        prev_link = paginator.get_previous_link()
        
        if next_link is not None:
            pages['next_page'] = next_link
        if prev_link is not None:
            pages['prev_page'] = prev_link
            
        return Response({'msg':'Artists list returend successfully.', **pages, 'status':200, 'data':serializers.data, 'total':allArtists.count()}, status=status.HTTP_200_OK)
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['GET'])
def get_one_artist(request:Request, qset:Optional[str]=None) -> Response:
    """
        - Get artist data from db 
        -METHOD : GET
        -Returns list of the artist with fields id, name, image, realname, bio
        -supports params for better searching 
    """
    try :
        
        
        if not qset : 
            return Response({'msg':'Artist found successfully.', 'status':200, 'data':""} , status=status.HTTP_200_OK)
       
        artist = ArtistsModel.objects.filter(Q(name__icontains = qset) | Q(id__icontains = qset))
        serializers = GetArtitstsSerialiazer(artist, many=True)
    
        return Response({'msg':'Artist found successfully.', 'status':200, 'data':serializers.data} , status=status.HTTP_200_OK)
        
    except ArtistsModel.DoesNotExist:
        return Response({'msg':'The artist not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['POST'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_artist(request:Request) -> Response:
    """
        - Add artist into database by reqeust.data info
        - METHOD : POST
        - Json schema : {'name':, 'image':, 'realname':, 'bio':}
        - Supported image : jpg, png, jpeg
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data 
    
    try:
        
        if len(data) < 1 :
            return Response({'msg':'Add values to fields of artist.', 'essential-fields':'name, image', 'optional-fields':'realname, bio', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'name' not in data or len(data['name']) < 1 :
            return Response({'msg':'Artist name can not be empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'image' not in data or  len(data['image']) == 0 or len(data.getlist('image')) > 1 :
            return Response({'msg':'Provide one image for the artist.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
        
        if 'image' in data and path.splitext(data['image'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
            return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = ArtistsModel.objects.get(name = data['name'])
        return Response({'msg':'Artist already exits.', 'status':302}, status=status.HTTP_302_FOUND)
    
    except ArtistsModel.DoesNotExist: 
        serializers = CreateArtistsSerialiazer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({'msg':'Artist added successfully.' , 'status':201, 'data':serializers.data} , status=status.HTTP_201_CREATED)
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['DELETE'])
@permission_classes([Is_superadmin])
def delete_artist(request:Request, id:int) -> Response:
    """
        - Delete artist from database by reqeust.data info
        - METHOD : PUT
        - Json schema : {'id':'id'}
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
        
        if not id:
            return Response({'msg':'Artist id is required.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = ArtistsModel.objects.get(pk = id)

        if artist.image.path:
            artistimage = artist.image.path
            os.remove(artistimage)
            
        artist.delete()
    
        return Response({'msg':'Artists deleted successfully.', 'status':200,}, status=status.HTTP_200_OK)
    
    except ArtistsModel.DoesNotExist:
        return Response({'msg':'Artist not found exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['PUT'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def update_artist(request:Request) -> Response:
    
    """
        - Update artist into database by reqeust.data info
        - METHOD : PUT
        - Json schema : {'id':'id', 'name':Artist-name, 'image':Artist-image, 'realname':Artist-realname, 'bio':Artist-bio}
        - Supported image : jpg, png, jpeg
        * Only admin's and super-admin's call this endpoint
    """
    data = request.data
    try:
       
        if len(data) == 0  or not len(data) > 1 :
            return Response({'msg':'Add values to fields of artist to update them.', 'essential-field':'id', 'optional-fields':'name, image, realname, bio', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data or len(data['id']) == 0  or len(data.getlist('id')) > 1:
            return Response({'msg':'Provide  one artist id to update artist data.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'name' in data and len(data['name']) == 0 or len(data.getlist('name')) > 1:
            return Response({'msg':'fields has no valid value.', 'field':'name', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'image' in data :
            if len(data['image']) == 0 or len(data.getlist('image')) > 1 :
                return Response({'msg':'Provide one image for the artist.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
            
            if path.splitext(data['image'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
                    return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
                  
        artist = ArtistsModel.objects.get(pk = data['id'])
        if artist.name == str(data['name']):
            return Response ({'msg':'artist name exists.', 'status':302}, status=status.HTTP_302_FOUND)
        
        
        serializers = UpdateDataArtistSerializer(artist , data=data, partial=True)
        if serializers.is_valid():
            if 'image' in data:
                image_path = path.join(settings.MEDIA_ROOT, artist.image.path)
                os.remove(image_path)
            serializers.save()
            
            return Response({'msg':'Artist data updated.' , 'status':200, 'data':serializers.data}, status=status.HTTP_200_OK)
       
    except ArtistsModel.DoesNotExist:
        return Response({'msg':'The artist does not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







        