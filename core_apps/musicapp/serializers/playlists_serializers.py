from rest_framework import serializers
from time import time


from ..models.playlists import PlaylistModel
from ..models.musics import MusicModel



class CreatePlayListSerializers(serializers.ModelSerializer):
    music_id = serializers.PrimaryKeyRelatedField(required=False, queryset=MusicModel.objects.all(), many=True)
    totaltracks = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    
    class Meta:
        model = PlaylistModel
        fields = ['id', 'title', 'cover', 'public_playlist', 'music_id', 'totaltracks', 'description']
        read_only_fields =['id']


    def create(self, validated_data):
        
        music_id = validated_data.pop('music_id', [])
        user = self.context['request'].user
        
        if validated_data['public_playlist'] >= 1:
            validated_data['public_playlist'] = 1
            
        playlist = PlaylistModel.objects.create(**validated_data)
        
        if music_id:
            playlist.music_id.add(*music_id)
            
        if user:
            user.playlists.add(playlist)
            
        if playlist :
            return playlist



    def to_representation(self, instance):
        
        music_info = []
        music = instance.music_id.all()
        for i in music:
            music_info.append([i.pk, i.title, i.musicfile.url, i.musiccover.url])
  
        user_id = self.context['request'].user
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = music_info
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at

        return req









class UpdatePlayListSerializers(serializers.ModelSerializer):

    class Meta:
        model = PlaylistModel
        fields = ['id', 'title', 'cover', 'public_playlist', 'music_id', 'totaltracks', 'description']
        read_only_fields = ['id',]
        
    def update(self, instance, validated_data):
        try:
          
            music_id = validated_data.pop('music_id', [])
            for attr , value in validated_data.items():
                setattr(instance, attr, value)
            
            instance.save()
            
            return instance
        
        except Exception as err:
            pass

        
    def to_representation(self, instance):
        
        music_info = []
        music = instance.music_id.all()
        for i in music:
            music_info.append([i.pk, i.title, i.musicfile.url, i.musiccover.url])
  
        user_id = self.context['request'].user
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = music_info
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at

        return req




    
    
    













class GetAllListsSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlaylistModel
        fields = ['id', 'title', 'music_id', 'cover', 'public_playlist',  'totaltracks', 'description']
        read_only_fields =['id']
        
    def to_representation(self, instance):
        
        music_info = []
        music = instance.music_id.all()
        for i in music:
            music_info.append([i.pk, i.title, i.musicfile.url, i.musiccover.url])
  
        user_id = self.context['request'].user
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = music_info
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at

        return req
    
    
class GetAllPublicListsSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlaylistModel
        fields = ['id', 'title', 'music_id', 'cover',  'totaltracks', 'description']
        read_only_fields =['id']
        
    def to_representation(self, instance):
        
        music_info = []
        music = instance.music_id.all()
        for i in music:
            music_info.append([i.pk, i.title, i.musicfile.url, i.musiccover.url])
  
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url
        req['playlist_public'] = 'public'
        req['musics'] = music_info
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at

        return req
        