
from urllib.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from loguru import logger
from django.db.models import Q
from django.conf import settings
from os import path
import os
from typing import Optional



from ..serializers.artists_serializers import CreateArtistsSerialiazer, GetArtitstsSerialiazer, UpdateDataArtistSerializer
from ..models.artists import ArtistsModels
from ..perms_manager import AllowAuthenticatedAndAdminsAndSuperAdmin , Is_superadmin



@api_view(['POST'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def add_artist(request:Request) -> Response:
    
    """
        -This function take the given info about the artist and save it into database
            #- METHOD : POST
            #- artist data scheme : {'name':Artist-name, 'image':Artist-image, 'realname':Artist-realname, 'bio':Artist-bio}
            #- supported image : jpg, png, jpeg

    """
    data = request.data 
    
    try:
        if len(data) == 0 :
            return Response({'msg':'Add this fields to add artist.', 'essential-fields':'name, image', 'optional-fields':'realname, bio', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'name' not in data or len(data['name']) < 1 :
            return Response({'msg':'Artist name can not be empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'image' not in data or  len(data['image']) == 0 or len(data.getlist('image')) > 1 :
            return Response({'msg':'Provide one image for the artist.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
        
        
        if 'image' in data and path.splitext(data['image'].name)[-1] not in ['.jpg', '.png', '.jpeg']:
            return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = ArtistsModels.objects.get(name = data['name'])
        
        return Response({'msg':'Artist already exits.', 'status':302}, status=status.HTTP_302_FOUND)
    
    except ArtistsModels.DoesNotExist: 
        serializers = CreateArtistsSerialiazer(data=data)
        if serializers.is_valid():
            serializers.save()
            logger.info(f'New artist added, Artitst-data:{str(serializers.data)}')
            return Response({'msg':'Artist added successfully.' , 'status':200, 'artist_info':serializers.data} , status=status.HTTP_201_CREATED)
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['PUT'])
@permission_classes([AllowAuthenticatedAndAdminsAndSuperAdmin])
def update_artist(request:Request) -> Response:
    
    """
        -This function change the given info about the artist and then updating it into database
            #- METHOD : PUT
            #- artist data scheme : {'id':Artist-id, 'name':Artist-name, 'image':Artist-image, 'realname':Artist-realname, 'bio':Artist-bio}
            #- supported image : jpg, png, jpeg
    """
    data = request.data
    try:
        
        if len(data) == 0  or not len(data) > 1 :
            return Response({'msg':'Add this fields to update the artist.', 'essential-field':'id', 'optional-fields':'name, image, realname, bio', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' not in data or len(data['id']) ==0  or len(data.getlist('id')) > 1:
            return Response({'msg':'Provide artist pk to update artist info.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'name' in data and len(data['name']) == 0 :
            return Response({'msg':'fields has no valid value.', 'field':'name', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
         
        if 'image' in data :
            
            if len(data['image']) == 0 or len(data.getlist('image')) > 1 :
                return Response({'msg':'Provide one image for the artist.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
            
            if path.splitext(data['image'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
                    return Response({'msg':'Image type is not supported.', 'supported-image':'jpg, png, jpeg', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
                

            
        artist = ArtistsModels.objects.get(pk = data['id'])
        
        serializers = UpdateDataArtistSerializer(artist , data=data, partial=True)
        if serializers.is_valid():
            if 'image' in data:
                
                image_path = path.join(settings.MEDIA_ROOT, artist.image.path)
                os.remove(image_path)
            serializers.save()
            
            logger.info(f'Artist info update , artist-new-info :{str(serializers.data)} ')
            return Response({'msg':'Artist data updated.' , 'status':200, 'artist-updated':serializers.data}, status=status.HTTP_200_OK)
       
    except ArtistsModels.DoesNotExist:
        return Response({'msg':'The artist does not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












@api_view(['GET'])
def get_all_artists(request:Request) -> Response:
    """
        -This function return's all artist's information 
            #- METHOD : GET
            #- Returns list of all artist with fields id, name, image, realname, bio
            #- supports params for better searching 
    """
    try :
        params = request.query_params
        default_order = '-name'
        if 'order' in params :
            default_order = params['order']
            
        allArtists = ArtistsModels.objects.all().order_by((default_order))
        serializers = GetArtitstsSerialiazer(allArtists , many=True)
        logger.info('All artists requested')
        return Response({'msg':'Artists list.', 'status':200, 'artists':serializers.data, 'total-artists':allArtists.count()}, status=status.HTTP_200_OK)
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['GET'])
def get_one_artist(request:Request, name:Optional[str]=None) -> Response:
    """
        -This function returns artist info based on the id and name of the artist
        # if the path contains artist name after the URL://v1/api/artist/aritst-name  it returns the artist info
        # else you can send these info's from the body in request.body
        
        #-METHOD : GET
        #-Returns list of all artist with fields id, name, image, realname, bio
        #-supports params for better searching 
    """
    try :
        data = request.data 
        info_dict = {}
        if not name: 
            artist_name = data.get('name' , None)
            aritst_id = data.get('id' , None)
            
            if artist_name and not aritst_id :
                info_dict['name'] = artist_name
            elif aritst_id and not artist_name:
                info_dict['pk'] = aritst_id
                
            elif artist_name and aritst_id :
                return Response({'msg':'Only provide name or id not both.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg':'Provide artist info name or pk.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)    
        else:  
            info_dict['name'] = name

        artist = ArtistsModels.objects.get(Q(**info_dict))
        serializers = GetArtitstsSerialiazer(artist)
        logger.info(f'artist data asked : {str(serializers.data)}')
        return Response({'msg':'Artist info found successfully.', 'status':200, 'artist-info':serializers.data} , status=status.HTTP_200_OK)
    
    except ArtistsModels.DoesNotExist:
        return Response({'msg':'The artist not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['DELETE'])
@permission_classes([Is_superadmin])
def delete_artist(request:Request):
    """
        -This function removes the artist by it's id 
        ## This is critical , know how to use this , this causes info lost or missing
        
        #- METHOD : DELETE
        #- Removes the artist from the database and also local storage
        
    """
    data = request.data
    try:
        
        if 'id' not in data:
            return Response({'msg':'Artist id is required.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' in data and  all(i.strip()=='' for i in data['id']) :
            return Response({'msg':'id field is empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = ArtistsModels.objects.get(pk = data['id'])
        aritst_info  = {}
        aritst_info['id'] = artist.pk
        aritst_info['name'] = artist.name
        aritst_info['image'] = artist.image.url
        aritst_info['realname'] = artist.realname
        aritst_info['bio'] = artist.bio
        
        if artist.image.path:
            artistimage = artist.image.path
            os.remove(artistimage)
            
        artist.delete()
        logger.info(f'Artist requested  deleted, artist-info : {artist.pk} - {artist.name}')
        return Response({'msg' : 'Artists deleted successfully.', 'artist-deleted':aritst_info ,'status':200}, status=status.HTTP_200_OK)
    
    except ArtistsModels.DoesNotExist:
        return Response({'msg':'Artist not found exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




        