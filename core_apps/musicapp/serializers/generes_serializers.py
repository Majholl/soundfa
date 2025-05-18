from rest_framework import serializers
from loguru import logger
from time import time 

from ..models.genres import GenereModel
from ..models.albums import AlbumModel
from ..models.artists import ArtistsModel
from ..models.musics import MusicModel



class CreateGenreSerializers(serializers.ModelSerializer):
    """
        - Serializer for validting genere data to add in database
        - Based on : Genere model
        - METHOD : POST
        - Create genere object in MYSQL db
        - Add relation to the artist , music , album
    """
    
    artist_id = serializers.PrimaryKeyRelatedField(required=False, queryset=ArtistsModel.objects.all(), many=True)
    music_id = serializers.PrimaryKeyRelatedField(required=False, queryset=MusicModel.objects.all(), many=True)
    album_id = serializers.PrimaryKeyRelatedField(required=False, queryset=AlbumModel.objects.all(), many=True)
    description = serializers.CharField(required=False)
    cover = serializers.FileField(required=False)
    class Meta:
        model = GenereModel
        fields = ['name', 'description', 'artist_id', 'music_id', 'album_id', 'cover']
        
        
    def create(self, validated_data):
        try:
            
            artist_id = validated_data.pop('artist_id', [])
            music_id = validated_data.pop('music_id', [])
            album_id = validated_data.pop('album_id', [])
            
            genere = GenereModel.objects.create(**validated_data)
            
            if artist_id:
                genere.artist_id.set(artist_id)
            
            if music_id:
                genere.music_id.set(music_id)
                
            if album_id:
                genere.album_id.set(album_id)
                            
            return genere
            
        except Exception as err:
            pass
        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['cover'] = instance.cover.url if instance.cover else None
        req['description'] = instance.description
        req['artists'] = instance.artist_id.values('id', 'name')
        req['musics'] = instance.music_id.values('id', 'title')
        req['albums'] = instance.album_id.values('id', 'title')
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        
        return req
    





class AddArtistToGenere(serializers.ModelSerializer):
    """
        - Serializer for increase artists of generes
        - Based on : Genere model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    artist_id = serializers.PrimaryKeyRelatedField(queryset=ArtistsModel.objects.all(), many=True)

    class Meta:
        model = GenereModel
        fields = ['id', 'artist_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['artist_id']:
            instance.artist_id.add(i.pk)
       

        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['description'] = instance.description
        req['artists'] = instance.artist_id.values('id', 'name')
        req['updated_at'] = instance.updated_at
        
        return req
    







class RemoveArtistToGenere(serializers.ModelSerializer):
    """
        - Serializer for decrease artists of generes
        - Based on : Genere model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    artist_id = serializers.PrimaryKeyRelatedField(queryset=ArtistsModel.objects.all(), many=True)

    class Meta:
        model = GenereModel
        fields = ['id', 'artist_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['artist_id']:
            instance.artist_id.remove(i.pk)
       

        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['description'] = instance.description
        req['artists'] = instance.artist_id.values('id', 'name')
        req['updated_at'] = instance.updated_at
        
        return req
    









































class UpdateGenereSerializers(serializers.ModelSerializer):
    """
        - Serializer for validting genere data to add in database
        - Based on : Genere model
        - METHOD : PUT
        - Update genere object in MYSQL db
        - Update relation to the artist and musics and album
    """
    class Meta:
        model = GenereModel
        fields = ['id', 'name', 'generecover', 'artist_id', 'music_id','album_id', 'description']
        read_only_fields = ['id',]
        
    def update(self, instance, validated_data):
        try:
            if 'artist_id' in validated_data:
                validated_data.pop('artist_id')
                
            if 'music_id' in validated_data:
                validated_data.pop('music_id')
            
            if 'album_id' in validated_data:
                validated_data.pop('album_id')
            
            for attr , value in validated_data.items():
                setattr(instance, attr, value)
            instance.updated_at = int(time())
            instance.save()
            
            return instance
        
        except Exception as err:
            print(err)

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['cover'] = instance.generecover.url
        req['description'] = instance.description
        req['artists'] = instance.artist_id.values('id', 'name')
        req['musics'] = instance.music_id.values('id', 'title')
        req['albums'] = instance.album_id.values('id', 'title')
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        
        return req
    



class GetAllGenereSerializers(serializers.ModelSerializer):
    """
        - Serializer for retruning genere data
        - Based on : genere model
        - METHOD : GET
    """
    class Meta:
        model = GenereModel
        fields = ['id', 'name', 'description', 'artist_id', 'music_id', 'album_id', 'generecover']
    
    def to_representation(self, instance):
        req = {}
        
        req['id'] = instance.pk
        req['name'] = instance.name
        req['cover'] = instance.generecover.url
        req['description'] = instance.description
        req['artists'] = instance.artist_id.values('id', 'name')
        req['musics'] = instance.music_id.values('id', 'title')
        req['albums'] = instance.album_id.values('id', 'title')
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        
        return req
    