from rest_framework import serializers



from ..models.genres import GenereModel
from ..models.albums import AlbumModel
from ..models.artists import ArtistsModel
from ..models.musics import MusicModel
from ..models.playlists import PlaylistModel


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
    playlist_id = serializers.PrimaryKeyRelatedField(required=False, queryset=PlaylistModel.objects.all(), many=True)

    description = serializers.CharField(required=False)
    cover = serializers.FileField(required=False)
    class Meta:
        model = GenereModel
        fields = ['name', 'description', 'artist_id', 'music_id', 'album_id', 'playlist_id', 'cover']
        
        
    def create(self, validated_data):
        try:
            
            artist_id = validated_data.pop('artist_id', [])
            music_id = validated_data.pop('music_id', [])
            album_id = validated_data.pop('album_id', [])
            playlist_id = validated_data.pop('playlist_id', [])
            
            genere = GenereModel.objects.create(**validated_data)
            
            if artist_id:
                genere.artist_id.set(artist_id)
            
            if music_id:
                genere.music_id.set(music_id)
                
            if album_id:
                genere.album_id.set(album_id)
                
            if playlist_id:
                genere.playlist_id.set(playlist_id)
                                          
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
        req['playlists'] = instance.playlist_id.values('id', 'title')
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
    










class AddMusicToGenere(serializers.ModelSerializer):
    """
        - Serializer for increase music of generes
        - Based on : Genere model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    music_id = serializers.PrimaryKeyRelatedField(queryset=MusicModel.objects.all(), many=True)

    class Meta:
        model = GenereModel
        fields = ['id', 'music_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['music_id']:
            instance.music_id.add(i.pk)
       
        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['description'] = instance.description
        req['musics'] = instance.music_id.values('id', 'title')
        req['updated_at'] = instance.updated_at
        
        return req
    




class RemoveMusicToGenere(serializers.ModelSerializer):
    """
        - Serializer for increase music of generes
        - Based on : Genere model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    music_id = serializers.PrimaryKeyRelatedField(queryset=MusicModel.objects.all(), many=True)

    class Meta:
        model = GenereModel
        fields = ['id', 'music_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['music_id']:
            instance.music_id.remove(i.pk)
       
        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['description'] = instance.description
        req['musics'] = instance.music_id.values('id', 'title')
        req['updated_at'] = instance.updated_at
        
        return req
    








class AddAlbumToGenere(serializers.ModelSerializer):
    """
        - Serializer for increase album of generes
        - Based on : Genere model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    album_id = serializers.PrimaryKeyRelatedField(queryset=AlbumModel.objects.all(), many=True)

    class Meta:
        model = GenereModel
        fields = ['id', 'album_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['album_id']:
            instance.album_id.add(i.pk)
       
        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['description'] = instance.description
        req['albums'] = instance.album_id.values('id', 'title')
        req['updated_at'] = instance.updated_at
        
        return req
    




class RemoveAlbumToGenere(serializers.ModelSerializer):
    """
        - Serializer for increase music of generes
        - Based on : Genere model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    album_id = serializers.PrimaryKeyRelatedField(queryset=AlbumModel.objects.all(), many=True)

    class Meta:
        model = GenereModel
        fields = ['id', 'album_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['album_id']:
            instance.album_id.remove(i.pk)
       
        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['description'] = instance.description
        req['albums'] = instance.album_id.values('id', 'title')
        req['updated_at'] = instance.updated_at
        
        return req
    












class AddPlaylistsToGenere(serializers.ModelSerializer):
    """
        - Serializer for increase album of generes
        - Based on : Genere model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    playlist_id = serializers.PrimaryKeyRelatedField(queryset=PlaylistModel.objects.all(), many=True)

    class Meta:
        model = GenereModel
        fields = ['id', 'playlists_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['playlists_id']:
            instance.playlist_id.add(i.pk)
       
        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['description'] = instance.description
        req['playlist'] = instance.playlist_id.values('id', 'title')
        req['updated_at'] = instance.updated_at
        
        return req
    




class RemovePlaylistToGenere(serializers.ModelSerializer):
    """
        - Serializer for increase music of generes
        - Based on : Genere model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    playlist_id = serializers.PrimaryKeyRelatedField(queryset=PlaylistModel.objects.all(), many=True)

    class Meta:
        model = GenereModel
        fields = ['id', 'playlist_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['playlist_id']:
            instance.playlist_id.remove(i.pk)
       
        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['description'] = instance.description
        req['playlist'] = instance.playlist_id.values('id', 'title')
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
        fields = ['id', 'name', 'cover', 'description']
        read_only_fields = ['id',]
        
    def update(self, instance, validated_data):
        try:
           
            for attr , value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            
            return instance
        
        except Exception as err:
            print(err)

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['name'] = instance.name
        req['cover'] = instance.cover.url if instance.cover else None
        req['description'] = instance.description
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
        fields = ['id', 'name', 'description', 'artist_id', 'music_id', 'album_id', 'cover']
    
    def to_representation(self, instance):
        req = {}
        
        req['id'] = instance.pk
        req['name'] = instance.name
        req['cover'] = instance.cover.url if instance.cover else None
        req['description'] = instance.description
        req['artists'] = instance.artist_id.values('id', 'name')
        req['musics'] = instance.music_id.values('id', 'title')
        req['albums'] = instance.album_id.values('id', 'title')
        req['playlists'] = instance.playlist_id.values('id', 'title')
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        
        return req
    