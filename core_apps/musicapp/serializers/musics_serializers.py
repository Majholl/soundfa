import os
from urllib import request
from rest_framework import serializers
from time import time

from ..models.artists import ArtistsModels
from ..models.musics import MusicModel





class CreateMusicSerializer(serializers.ModelSerializer):
    """
        -This class is for creating music into database 
        #- METHOD : POST
        #- Add music into database
        #- Represent data 
    """
    artist_id = serializers.PrimaryKeyRelatedField(queryset=ArtistsModels.objects.all(), many=True)
    musiccover = serializers.ImageField(required=False)
    
    class Meta:
        model = MusicModel
        fields = ['id', 'title' , 'musicfile', 'musiccover', 'duration', 'lyrics', 'artist_id']
    
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
        req['artists_id'] = instance.artist_id.values('id', 'name')
        req['musicfile'] = instance.musicfile.url
        
        if instance.duration : 
            req['duration'] = instance.duration
            
        if instance.lyrics : 
            req['lyrics'] = instance.lyrics
            
        if instance.musiccover :
            req['musiccover'] = instance.musiccover.url
            
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req
    












class UpdateMusicSerializer(serializers.ModelSerializer):
    """
        -This class is for updating music data into database
        #- METHOD : PUT
        #- Update music into database
        #- Represent data 
    """
    class Meta:
        model = MusicModel
        fields = ['id', 'duration', 'lyrics', 'musiccover']
    
    
    def update(self, instance, validated_data):
        
        try: 
            for atrr , value in validated_data.items():
                setattr(instance, atrr, value)
                
            instance.updated_at = int(time())     
            instance.save()  
            return instance
        
        except Exception as err:
            pass
    
    
    def to_representation(self, instance):
        req = {}

        req['id'] = instance.pk
        req['title'] = instance.title
        req['artists_id'] =  instance.artist_id.values('id', 'name')
        req['musicfile'] = instance.musicfile.url
        
        if instance.musiccover:
            req['musiccover'] = instance.musiccover.url
            
        if instance.duration:
            req['duration'] = instance.duration
            
        if instance.lyrics:
            req['lyrics'] = instance.lyrics
            
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req
    






class GetMusicByNameSerializer(serializers.ModelSerializer):
    """
        -This class called to returned musics info
            #- METHOD : GET 
            #- Get musics info 
            #- Represent data 
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
        req['musicfile-downloadable'] = self.get_download_url(instance)
        
        if instance.musiccover :
            req['musiccover']  = instance.musiccover.url
            
        if instance.duration : 
            req['duration']  = instance.duration
            
        if instance.lyrics : 
            req['lyrics']  = instance.lyrics
            
        req['artists']  = instance.artist_id.values('id', 'name') 
        req['created_at']  = instance.created_at   
        req['updated_at']  = instance.updated_at   
        
        return req