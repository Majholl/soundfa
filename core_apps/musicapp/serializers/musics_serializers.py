import os
from rest_framework import serializers
from time import time

from ..models.artists import ArtistsModel
from ..models.musics import MusicModel



class CreateMusicSerializer(serializers.ModelSerializer):
    """
        - Serializer for validting music data to add in database
        - Based on : Music model
        - METHOD : POST
        - Create Music object in MYSQL db
        - Add relation to the artist
    """
    artist_id = serializers.PrimaryKeyRelatedField(queryset=ArtistsModel.objects.all(), many=True)
    cover = serializers.ImageField(required=False)
    
    class Meta:
        model = MusicModel
        fields = ['id', 'title' , 'file', 'cover', 'duration', 'lyrics', 'artist_id']
    
    def create(self, validated_data):
        try:
            artists_id = validated_data.pop('artist_id', [])
            music = MusicModel.objects.create(**validated_data)
            music.artist_id.set(artists_id)
            return music
        
        except Exception as err:
            pass

    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['artists'] = instance.artist_id.values('id', 'name')
        req['file'] = instance.file.url 
        req['cover'] = instance.cover.url if instance.cover else None
        req['duration'] = instance.duration
        req['lyrics'] = instance.lyrics  
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req
    












class UpdateMusicSerializer(serializers.ModelSerializer):
    """
        - Serializer for validting music data to add in database
        - Based on : Music model
        - METHOD : PUT
        - Update Music object in MYSQL db
    """
    class Meta:
        model = MusicModel
        fields = ['id', 'duration', 'lyrics', 'cover']
    
    
    def update(self, instance, validated_data):
        try: 
            for atrr , value in validated_data.items():
                setattr(instance, atrr, value)
                
            instance.save()  
            return instance
        
        except Exception as err:
            pass
    
    
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['file'] = instance.file.url 
        req['cover'] = instance.cover.url if instance.cover else None
        req['duration'] = instance.duration
        req['lyrics'] = instance.lyrics  
        req['artists'] = instance.artist_id.values('id', 'name')
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req






class GetMusicByNameSerializer(serializers.ModelSerializer):
    """
        - Serializer for retruning music data
        - Based on : Music model
        - METHOD : GET
    """
    
    download_url = serializers.SerializerMethodField()
    class Meta:
        model = MusicModel
        fields = ['id', 'title', 'musicfile', 'download_url', 'musiccover', 'duration', 'lyrics', 'artist_id', 'created_at', 'updated_at']
    
    
    def get_download_url(self, obj):
        request = self.context.get('request')
        filename = os.path.basename(obj.musicfile.name)
        return request.build_absolute_uri(f'download/music/{filename}')
        
        
    def to_representation(self, instance):
        req = {}
        pk = instance.pk

        req['id'] = pk     
        req['title'] = instance.title
        req['musicfile']  = instance.musicfile.url
        req['cover']  = instance.musiccover.url
        req['duration']  = instance.duration
        req['genere'] = instance.genere_id.values('name',)
        req['lyrics']  = instance.lyrics    
        req['artists']  = instance.artist_id.values('id', 'name') 
        req['musicfile-downloadable'] = self.get_download_url(instance)
        req['created_at']  = instance.created_at   
        req['updated_at']  = instance.updated_at   
        
        return req