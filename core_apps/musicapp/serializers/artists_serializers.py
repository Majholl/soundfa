from rest_framework import serializers
from loguru import logger
from time import time 

from ..models.artists import ArtistsModel
from core_apps.musicapp.models import artists



class CreateArtistsSerialiazer(serializers.ModelSerializer):
    """
        -This class is for adding artist into database
            #- METHOD : POST 
            #- Add one artist 
            #- Represent data 
    """
    realname = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    
    class Meta:
        model = ArtistsModel
        fields = ["name", "realname", "bio", "image"]
    
    def create(self, validated_data):
        try:
            aritsts = ArtistsModel.objects.create(**validated_data)
            if aritsts :
                logger.info(f'New Artist added , Artist : {str(validated_data)}')
                return aritsts
        
        except Exception as err:
            logger.error(f'Error during adding artits : Error {str(err)}')
            
            
    def to_representation(self, instance):
        req = {}
        pk = instance.pk 
        try:
            req['id'] = pk
            
            req['name'] = instance.name
            req['image'] = instance.image.url
            
            if instance.bio :
               req['bio'] = instance.bio
               
            if instance.realname :
               req['realname'] = instance.realname
            
            req['created_at'] = instance.created_at
            
        except Exception as err:
            logger.error(f'Error during representing data : Error {str(err)}')
        
        return req
        
        
                    
class UpdateDataArtistSerializer(serializers.ModelSerializer):
    """
        -This class is useing for updating info of the artist 
            #- METHOD : PUT 
            #- Update artist info 
            #- Represent data 
    """
    class Meta:
        model = ArtistsModel
        fields = ["id", "name", "image", "realname", "bio"]
        read_only_fields = ["id",]
        
        
    def update(self, instance, validated_data):
        try:
            for attr , value in validated_data.items():
                setattr(instance , attr, value)
            instance.updated_at = int(time())    
            instance.save()
            
            logger.info(f'Artist info update, Artist : {str(validated_data)}')

        except Exception as err:
            logger.info(f'Error during updating artist info : Error {str(err)}')
            
        return instance        
        
        
    def validate(self, data):
           self._validated_data = data
           return data
       
        
    def to_representation(self, instance):
        data = self._validated_data
        req = {}
        pk = instance.pk
        
        req['id'] = pk
        
        if 'name' in data or instance.name:    
            req['name'] = instance.name
            
        if 'realname' in data or instance.realname: 
            req['realname'] = instance.realname
            
        if 'bio' in data or instance.bio:     
            req['bio'] = instance.bio
            
        if 'image' in data or instance.image: 
            req['image'] = instance.image.url
          
        req['created_at'] = instance.created_at
        req['update_at'] = instance.updated_at
        
        return req
     
     
        
             
             
class GetArtitstsSerialiazer(serializers.ModelSerializer):
    """
        -This class called to returned artist or artists information 
            #- METHOD : GET 
            #- Get artist info 
            #- Represent data 
    """
    class Meta:
        model = ArtistsModel
        fields = ["id", "name", "realname", "bio", "image"]
        read_only_fields = ["id"]
        
    def to_representation(self, instance):
        req = {}
        pk = instance.pk
        
        req['id'] = pk
            
        req['name'] = instance.name
        req['image'] = instance.image.url
        req['bio'] = instance.bio
        req['realname'] = instance.realname
        req['created_at'] = instance.created_at 
        req['updated_at'] = instance.updated_at

        return req