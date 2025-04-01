from rest_framework import serializers
from loguru import logger
from time import time 

from ..models.artists import ArtistsModels




class CreateArtistsSerialiazer(serializers.ModelSerializer):
    """
    -This class is for adding artists into database
    
    """

    realname = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    
    class Meta:
        model = ArtistsModels
        fields =["name", "realname", "bio", "image"]
    
    def create(self, validated_data):
        try:
            aritsts = ArtistsModels.objects.create(**validated_data)
            if aritsts :
                return aritsts
        
        except Exception as err:
            logger.error(f'Error during adding artits to db : Error {str(err)}')
            
            
    def to_representation(self, instance):
        req = {}
        pk = instance.pk 
        try:
            if not pk in req:
                req[pk] = {}
            
            req[pk]['name'] = instance.name
            req[pk]['image'] = instance.image.url
            
            if instance.bio :
               req[pk]['bio'] = instance.bio
            if instance.realname :
               req[pk]['realname'] = instance.realname
            
            req[pk]['created_at'] = instance.created_at
            
        except Exception as err:
            pass
        
        return req
        
        
        
               
class UpdateDataArtistSerializer(serializers.ModelSerializer):
    """
        -This class is useing for updating info of the artist 
    """
    class Meta:
        model = ArtistsModels
        fields = ["id", "name", "image", "realname", "bio"]
        read_only_fields = ['id']
        
        
    def update(self, instance, validated_data):
        try:
            for attr , value in validated_data.items():
                setattr(instance , attr, value)
            instance.updated_at = int(time())      
            instance.save()

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
        
        if not pk in req : 
            req[pk] = {}
        if 'name' in data :    
            req[pk]['name'] = instance.name
            
        if 'realname' in data : 
            req[pk]['realname'] = instance.realname
            
        if 'bio' in data :     
            req[pk]['bio'] = instance.bio
            
        if 'image' in data : 
            req[pk]['image'] = instance.image.url
          
        req[pk]['update_at'] = instance.updated_at
        
        return req
     
     
        
        
        
        
        
        
        
class GetArtitstsSerialiazer(serializers.ModelSerializer):
    """
        -This class called to returned artist or artists information 
    """
    class Meta:
        model = ArtistsModels
        fields = ["id", "name", "realname", "bio", "image"]
        read_only_fields = ["id"]
        
    def to_representation(self, instance):
        req = {}
        pk = instance.pk
        if not pk in req:
            req[pk] = {}
            
        req[pk]['name'] = instance.name
        req[pk]['image'] = instance.image.url
        req[pk]['bio'] = instance.bio
        req[pk]['realname'] = instance.realname
        req[pk]['created_at'] = instance.created_at 
        req[pk]['updated_at'] = instance.updated_at

        return req