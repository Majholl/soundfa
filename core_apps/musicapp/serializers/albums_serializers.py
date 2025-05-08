from rest_framework import serializers
from loguru import logger
from time import time
from itertools import chain


from ..models.albums import AlbumModel
from ..models.artists import ArtistsModel
from ..models.musics import MusicModel
from ..models.genres import GenereModel




class CreateAlbumSerializers(serializers.ModelSerializer):
    """
        - Serializer for validting album data to add in database
        - Based on : Album model
        - METHOD : POST
        - Create album object in MYSQL db
        - Add relation to the artist and musics
    """
    
    artist_id = serializers.PrimaryKeyRelatedField(required=False, queryset=ArtistsModel.objects.all(), many=True)
    music_id = serializers.PrimaryKeyRelatedField(required=False, queryset=MusicModel.objects.all(), many=True)
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
            print(err)
        
        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['albumcover'] = instance.albumcover.url
        req['artists'] = instance.artist_id.values('id', 'name')
        req['musics'] = instance.music_id.values('id', 'title')
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req
    
    
    
    
    
    
    
    
class UpdateAlbumSerializers(serializers.ModelSerializer):
    """
        - Serializer for validting album data to add in database
        - Based on : Album model
        - METHOD : PUT
        - Update album object in MYSQL db
        - Update relation to the artist and musics
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
        req['artists'] = instance.artist_id.values('id', 'name')
        req['musics'] = instance.music_id.values('id', 'title')
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        
        return req
    
    
    
    
    
    
    
class GetAlbumByNameSerializer(serializers.ModelSerializer):
    
    """
        - Serializer for validting album data to get from database
        - Based on : Album model
        - METHOD : GET
        - Get album object in MYSQL db
        - Get relation to the artist and musics
    """
        
    class Meta:
        model = AlbumModel
        fields = ['id', 'title', 'albumcover', 'artist_id', 'music_id', 'totaltracks', 'description', 'created_at', 'updated_at',]
        read_only_fields = ["id"]
        
        
    def to_representation(self, instance):
        req = {}
        
        music_artist_info = {}
        
        music_info = instance.music_id.values('id', 'title', 'duration', 'musiccover', 'musicfile')
       
        for i in instance.music_id.values_list('id', flat=True):
            music = MusicModel.objects.get(id = i)
            artist_data = music.artist_id.values('id', 'name', 'realname', 'bio' ,'image')
       
        for i in music_info :
            i['music_id'] = i['id']
            i.pop('id')
            music_artist_info.update(i)
        
        for j in artist_data:
            j['artist_id'] = j['id']
            j.pop('id')
            music_artist_info.update(j)
                  
            
        req['id'] = instance.pk
        req['title'] = instance.title
        req['albumcover'] = instance.albumcover.url
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['artists'] = instance.artist_id.values('id', 'name', 'image')
        req['musics'] = music_artist_info
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        
        return req
    
    
    