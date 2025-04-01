from rest_framework import serializers

from ..models.artists import ArtistsModels
from ..models.musics import MusicModel
from time import time





class CreateMusicSerializer(serializers.ModelSerializer):
    """
        -This class is for creating music into database 
    """
    artist_id = serializers.PrimaryKeyRelatedField(queryset=ArtistsModels.objects.all(), many=True)
    musiccover = serializers.ImageField(required=False)
    
    class Meta:
        model = MusicModel
        fields = ['id', 'title' , 'musicfile', 'musiccover', 'artist_id']
    
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
        artists_id = []
        for i in instance.artist_id.all():
            artists_id.append({'id':i.pk, 'name':i.name})
            
        req['id'] = instance.pk
        req['title'] = instance.title
        req['artists_id'] = artists_id
        req['musicfile'] = instance.musicfile.url
        if instance.musiccover :
            req['musiccover'] = instance.musiccover.url
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req
    












class UpdateMusicSerializer(serializers.ModelSerializer):
    """
        -This class is for updating music data into database
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
        artists_id = []
        for i in instance.artist_id.all():
            artists_id.append({'id':i.pk, 'name':i.name})
            
        req['id'] = instance.pk
        req['title'] = instance.title
        req['artists_id'] = artists_id
        req['musicfile'] = instance.musicfile.url
        
        if instance.musiccover :
            req['musiccover'] = instance.musiccover.url
        if instance.duration:
            req['duration'] = instance.duration
        if instance.lyrics:
            req['lyrics'] = instance.lyrics
            
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req
    






class GetMusicByNameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MusicModel
        fields = ['id', 'title', 'musicfile', 'musiccover', 'duration', 'lyrics', 'artist_id', 'created_at', 'updated_at']
    
    
    
    def to_representation(self, instance):
        req = {}
        artist_id = []
        for i in instance.artist_id.all():
            artist_id.append({'id':i.pk, 'name':i.name})
            
        pk = instance.pk
        if pk not in req:
            req[pk] = {}
            
        req[pk]['title'] = instance.title
        req[pk]['musicfile']  = instance.musicfile.url
        
        if instance.musiccover :
            req[pk]['musiccover']  = instance.musiccover.url
            
        req[pk]['duration']  = instance.duration
        req[pk]['lyrics']  = instance.lyrics
        req[pk]['artists']  = artist_id   
        req[pk]['created_at']  = instance.created_at   
        req[pk]['updated_at']  = instance.updated_at   
        
        return req