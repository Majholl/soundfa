from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from loguru import logger
from django.db.models import Q
from django.conf import settings
from os import path
import os
from typing import Optional

from ..serializers.artists_serializers import CreateArtistsSerialiazer, GetArtitstsSerialiazer, UpdateDataArtistSerializer
from ..models.artists import ArtistsModels




@api_view(['POST'])
def add_artist(request) -> Response:
    
    """
        -This function take the given info about the artist and save it into database
    """
    data = request.data 
    try:
        if not 'name' in data or len(data['name']) <1 :
            return Response({'msg':'Artist name can not be empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'image' in data or len(data['image']) <=1:
            return Response({'msg':'Artist image must be only one.', 'status':400} , status=status.HTTP_400_BAD_REQUEST) 
         
        if path.splitext(data['image'].name)[-1] not in ['.jpg', '.png', '.jpeg']:
            return Response({'msg':'Image type is not supported.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = ArtistsModels.objects.get(name = data['name'])
        return Response({'msg':'Artist already exits.', 'status':302}, status=status.HTTP_302_FOUND)
    
    except ArtistsModels.DoesNotExist: 
        serializers = CreateArtistsSerialiazer(data=data)
        
        if serializers.is_valid():
            serializers.save()
            logger.info(f'New artist added , Artitst-data:{str(serializers.data)}')
            return Response({'msg':'Artist added successfully.' , 'status':200, 'artist_info':serializers.data} , status=status.HTTP_201_CREATED)
    
    except Exception as err:    
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['PUT'])
def update_artist(request) -> Response:
    
    """
        -This function change the given info about the artist and then updating it into database
    """
    data = request.data
    try:
        if 'id' not in data or len(data['id']) <1 :
            return Response({'msg':'Provide artist pk to update artist info.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = ArtistsModels.objects.get(pk = data['id'])
        
        serializers = UpdateDataArtistSerializer(artist , data=data, partial=True)
        if serializers.is_valid():
            if 'image' in data:
                if path.splitext(data['image'].name)[-1] not in ['.jpg', '.png', '.jpeg'] :
                    return Response({'msg':'Image type is not supported.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
                image_path = path.join(settings.MEDIA_ROOT, artist.image.path)
                os.remove(image_path)
            serializers.save()
            
            logger.info(f'Artist data updated to -> {str(serializers.data)} ')
            return Response({'msg':'Artist info updated.' , 'status':200, 'artist-info-updated':serializers.data}, status=status.HTTP_200_OK)
       
    except ArtistsModels.DoesNotExist:
        return Response({'msg':'The artist does not exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










@api_view(['GET'])
def get_all_artists(request) -> Response:
    """
        -This function return's all artist's information 
    """
    try :
        allArtists = ArtistsModels.objects.all().order_by(('-created_at'))
        serializers = GetArtitstsSerialiazer(allArtists , many=True)
        logger.info('All artists requested')
        return Response({'msg':'Artists list.', 'status':200, 'artists':serializers.data, 'total-artists':allArtists.count()}, status=status.HTTP_200_OK)
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['GET'])
def get_one_artist(request, name:Optional[str]=None) -> Response:
    """
        -This function returns artist info based on the id and name of the artist
        ## if the path contains artist name after the URL://v1/api/artist/aritst-name  it returns the artist info
        ## else you can send these info's from the body in request.body
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
def delete_artist(request):
    data = request.data
    try:
        
        if 'id' not in data:
            return Response({'msg':'Artist id is required.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'id' in data and len(data.getlist('id')) <1:
            return Response({'msg':'id field is empty.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = ArtistsModels.objects.get(pk = data['id'])
        if artist.image.path:
            artistimage = artist.image.path
            os.remove(artistimage)
            
        artist.delete()
        logger.info(f'Artist requested for deletion, artist-info : {artist.pk} - {artist.name}')
        return Response({'msg' : 'Artists deleted successfully.', 'status':200}, status=status.HTTP_200_OK)
    
    except ArtistsModels.DoesNotExist:
        return Response({'msg':'Artist not found exits.', 'status':404}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




        