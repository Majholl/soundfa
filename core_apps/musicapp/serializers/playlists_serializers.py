from rest_framework import serializers


from ..models.playlists import PlaylistModel
from ..models.musics import MusicModel



class CreatePlayListSerializers(serializers.ModelSerializer):
    """
        - Serializer for validting playlist data to add in database
        - Based on : Playlist model
        - METHOD : POST
        - Create Playlist object in MYSQL db
        - Add relation to the music
    """
    music_id = serializers.PrimaryKeyRelatedField(required=False, queryset=MusicModel.objects.all(), many=True)
    description = serializers.CharField(required=False)
    
    class Meta:
        model = PlaylistModel
        fields = ['id', 'title', 'cover', 'public_playlist', 'music_id', 'description']
        read_only_fields =['id']


    def create(self, validated_data):
        
        music_id = validated_data.pop('music_id', [])
        user = self.context['request'].user
        

        if 'public_playlist' in validated_data and validated_data['public_playlist'] >= 1:
            validated_data['public_playlist'] = 1
            
        playlist = PlaylistModel.objects.create(**validated_data)
        playlist.count_totaltracks(len(music_id))
        
        if music_id:
            for i in [i.pk for i in music_id]:
                playlist.music_id.add(i)
            
        if user:
            user.playlists.add(playlist)
            
        if playlist :
            return playlist



    def to_representation(self, instance):
        
        user_id = self.context['request'].user
        
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url if instance.cover else None
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = [{'id' : i.id, 'title':i.title, 'file':i.file.url, 'cover': i.cover.url} for i in instance.music_id.all()]
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at

        return req
    




class AddMusicToPlaylist(serializers.ModelSerializer):
    """
        - Serializer for increase musics of playlists
        - Based on : Playlist model
        - METHOD : PATCH
        - Relation to the music
    """    
    music_id = serializers.PrimaryKeyRelatedField(queryset=MusicModel.objects.all(), many=True)

    class Meta:
        model = PlaylistModel
        fields = ['id', 'music_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
        existing_musics = [i['id'] for i in instance.music_id.values('id')]
        
        for i in validated_data['music_id']:
            instance.music_id.add(i.pk)
            
        musics_pk = [i.pk for i in validated_data['music_id']]

        ind = 0
        for i in musics_pk:
            if i not in existing_musics:
                ind +=1 
                
        instance.count_totaltracks(instance.totaltracks + ind)

        return instance

    def to_representation(self, instance):
        
        user_id = self.context['request'].user
        req = {}
        req['id'] = instance.pk
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = [{'id' : i.id, 'title':i.title, 'file':i.file.url, 'cover': i.cover.url} for i in instance.music_id.all()]
        req['totaltracks'] = instance.totaltracks
        req['updated_at'] = instance.updated_at

        return req
    



class RemoveMusicToPlaylist(serializers.ModelSerializer):
    """
        - Serializer for decrease musics of playlists
        - Based on : Playlist model
        - METHOD : PATCH
        - Relation to the music
    """    
    music_id = serializers.PrimaryKeyRelatedField(queryset=MusicModel.objects.all(), many=True)

    class Meta:
        model = PlaylistModel
        fields = ['id', 'music_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
        existing_musics = [i['id'] for i in instance.music_id.values('id')]
        
        for i in validated_data['music_id']:
            instance.music_id.remove(i.pk)
            
        musics_pk = [i.pk for i in validated_data['music_id']]

        ind = 0
        for i in musics_pk:
            if i  in existing_musics:
                ind +=1 
                
        instance.count_totaltracks(instance.totaltracks - ind)

        return instance

    def to_representation(self, instance):
        
        user_id = self.context['request'].user
        req = {}
        req['id'] = instance.pk
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = [{'id' : i.id, 'title':i.title, 'file':i.file.url, 'cover': i.cover.url} for i in instance.music_id.all()]
        req['totaltracks'] = instance.totaltracks
        req['updated_at'] = instance.updated_at

        return req







class UpdatePlayListSerializers(serializers.ModelSerializer):
    """
        - Serializer for update data of the playlists
        - Based on : Playlist model
        - METHOD : UPDATE
        - Relation to the music
    """  
    music_id = serializers.PrimaryKeyRelatedField(required = False, queryset = MusicModel.objects.all(), many=True)
    class Meta:
        model = PlaylistModel
        fields = ['id', 'title', 'cover', 'public_playlist', 'music_id', 'description']
        read_only_fields = ['id',]
        
    def update(self, instance, validated_data):
        try:
          
            music_id = validated_data.pop('music_id', [])
            for attr , value in validated_data.items():
                setattr(instance, attr, value)   
            instance.save()
            
            instance.music_id.clear()

            if music_id: 
                instance.music_id.set(music_id)
            instance.count_totaltracks(len(music_id))
                    
            return instance
        
        except Exception as err:
            pass

        
    def to_representation(self, instance):
        
        user_id = self.context['request'].user
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url if instance.cover else "null" 
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = [{'id' : i.id, 'title':i.title, 'file':i.file.url, 'cover': i.cover.url} for i in instance.music_id.all()]
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at

        return req
    
    
    
    













class GetAllListsSerializers(serializers.ModelSerializer):
    """
        - Serializer for get data of the playlists of the user
        - Based on : Playlist model
        - METHOD : GET
        - Relation to the music
    """  
    class Meta:
        model = PlaylistModel
        fields = ['id', 'title', 'music_id', 'cover', 'public_playlist', 'description']
        read_only_fields =['id']
        
    def to_representation(self, instance):
        
        user_id = self.context['request'].user
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url if instance.cover else "null"
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = [{'id' : i.id, 'title':i.title, 'file':i.file.url, 'cover': i.cover.url} for i in instance.music_id.all()]
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at

        return req
    
    
    
    
    
    
    
class GetAllPublicListsSerializers(serializers.ModelSerializer):
    """
        - Serializer for get data of the public playlists 
        - Based on : Playlist model
        - METHOD : GET
        - Relation to the music
    """  
    class Meta:
        model = PlaylistModel
        fields = ['id', 'title', 'music_id', 'cover', 'public_playlist', 'description']
        read_only_fields =['id']
        
    def to_representation(self, instance):
        
        user_id = self.context['request'].user
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url if instance.cover else "null"
        req['playlist_public'] = 'public' if instance.public_playlist == 1  else 'private'
        req['user'] = user_id.pk
        req['musics'] = [{'id' : i.id, 'title':i.title, 'file':i.file.url, 'cover': i.cover.url} for i in instance.music_id.all()]
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at

        return req
    
         