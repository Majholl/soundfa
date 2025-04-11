
from rest_framework import serializers
from loguru import logger
from time import time

from ..models.albums import AlbumModel
from ..models.artists import ArtistsModels
from ..models.musics import MusicModel
from ..models.genres import GenereModel




class CreateAlbumSerializers(serializers.ModelSerializer):
    """
        -This class is for adding album into database
            #- METHOD : POST 
            #- Add one album 
            #- Represent data 
    """
    
    artist_id = serializers.PrimaryKeyRelatedField(required=False, queryset=ArtistsModels.objects.all(), many=True)
    music_id = serializers.PrimaryKeyRelatedField(required=False, queryset=MusicModel.objects.all(), many=True)
    # genre_id = serializers.PrimaryKeyRelatedField(required=False, queryset=GenereModel.objects.all(), many=True)
    totaltracks = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    
    class Meta:
        model = AlbumModel
        fields = ['title', 'albumcover', 'artist_id', 'music_id', 'totaltracks', 'description']
        
    def create(self, validated_data):
        try:
  
            artist_id = validated_data.pop('artist_id', [])
            music_id = validated_data.pop('music_id', [])
            album = AlbumModel.objects.create(**validated_data)
            
            if artist_id : 
                album.artist_id.set(artist_id)
                
            if music_id : 
                album.music_id.set(music_id)
                
            if album:
                return album
            
        except Exception as err:
            pass
        
        
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        return req
    
    
    
    
    
    
    
    
class UpdateAlbumSerializers(serializers.ModelSerializer):
    """
        -This class is useing for updating info of the album 
            #- METHOD : PUT 
            #- Update album info 
            #- Represent data 
    """
    class Meta:
        model = AlbumModel
        fields = ['id', 'title', 'albumcover', 'artist_id', 'music_id', 'totaltracks', 'description']
        read_only_fields = ['id',]
        
    def update(self, instance, validated_data):
        try:
            if 'artist_id' in validated_data:
                
                validated_data.pop('artist_id')
            if 'music_id' in validated_data:
                validated_data.pop('music_id')
            
            for attr , value in validated_data.items():
                setattr(instance, attr, value)
            instance.updated_at = int(time())
            instance.save()
            
            return instance
        
        except Exception as err:
            pass

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['albumcover'] = instance.albumcover.url
        req['artist_id'] = instance.artist_id.values('id', 'name')
        req['music_id'] = instance.music_id.values('id', 'title')
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        
        return req
    
    
    
    
    
    
    
class GetAlbumByNameSerializer(serializers.ModelSerializer):
    
    """
        -This class called to returned artist or album information 
            #- METHOD : GET 
            #- Get album info 
            #- Represent data 
    """
        
    class Meta:
        model = AlbumModel
        fields = ['id', 'title', 'albumcover', 'artist_id', 'music_id', 'totaltracks', 'description', 'created_at', 'updated_at',]
        read_only_fields = ["id"]