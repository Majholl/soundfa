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
                return aritsts
    
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
        
        
        
        
        
                           
class UpdateDataArtistSerializer(serializers.ModelSerializer):
    """
        - Serializer for validting artist data to upating data
        - Based on : Artist model
        - METHOD : PUT
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
                
            instance.save()
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
        - Serializer for retruning artist data
        - Based on : Artist model
        - METHOD : GET
    """
    class Meta:
        model = ArtistsModel
        fields = ["id", "name", "realname", "bio", "image"]
        read_only_fields = ["id"]
        
    def to_representation(self, instance):
        req = {} 
        req['id'] = instance.id
        req['name'] = instance.name
        req['image'] = instance.image.url
        req['bio'] = instance.bio
        req['realname'] = instance.realname
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req