from rest_framework import serializers
from loguru import logger
from time import time 

from ..models.artists import ArtistsModel
from core_apps.musicapp.models import artists



class CreateArtistsSerialiazer(serializers.ModelSerializer):
    """
        - Serializer for validting artist data to add in database
        - Based on : Artist model
        - METHOD : POST
        - Create artist object in MYSQL db
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
                logger.info(f'New Artist added, {str(validated_data)}')
                return aritsts
        
        except Exception as err:
            pass
            
            
    def to_representation(self, instance):
        req = {} 
        req['id'] = instance.pk
        req['name'] = instance.name
        req['image'] = instance.image.url
        
        if instance.bio :
            req['bio'] = instance.bio
            
        if instance.realname :
            req['realname'] = instance.realname
        
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req
        
        
        
        
        
                           
class UpdateDataArtistSerializer(serializers.ModelSerializer):
    """
        - Serializer for validting artist data to upating data
        - Based on : Artist model
        - METHOD : POST
        - update artist object in MYSQL db
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
            logger.info(f'Artist data updateed, {str(validated_data)}')
            return instance      
        
        except Exception as err:
            pass
            
          
        
    def to_representation(self, instance):
        req = {} 
        req['id'] = instance.pk
        req['name'] = instance.name
        req['image'] = instance.image.url
        req['bio'] = instance.bio
        req['realname'] = instance.realname
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
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