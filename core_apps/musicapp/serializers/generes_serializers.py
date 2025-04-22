from rest_framework import serializers
from loguru import logger
from time import time 

from ..models.genres import GenereModel
from ..models.albums import AlbumModel
from ..models.artists import ArtistsModel
from ..models.musics import MusicModel



class CreateGenreSerializers(serializers.ModelSerializer):
    
    
    artist_id = serializers.PrimaryKeyRelatedField(required=False, queryset=ArtistsModel.objects.all(), many=True)
    music_id = serializers.PrimaryKeyRelatedField(required=False, queryset=MusicModel.objects.all(), many=True)
    album_id = serializers.PrimaryKeyRelatedField(required=False, queryset=AlbumModel.objects.all(), many=True)
    description = serializers.CharField(required=False)
    generecover = serializers.FileField(required=False)
    class Meta:
        model = GenereModel
        fields = ['name', 'description', 'artist_id', 'music_id', 'album_id', 'generecover']
        
        
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
        req = super().to_representation(instance)
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        return req
           
        






class GetAllGenereSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = GenereModel
        fields = ['id', 'name', 'description', 'artist_id', 'music_id', 'album_id', 'generecover']
        