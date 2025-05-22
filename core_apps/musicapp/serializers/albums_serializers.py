from rest_framework import serializers

from ..models.albums import AlbumModel
from ..models.artists import ArtistsModel
from ..models.musics import MusicModel





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
    description = serializers.CharField(required=False)
    
    class Meta:
        model = AlbumModel
        fields = ['title', 'cover', 'artist_id', 'music_id', 'description']
        
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
                album.count_totaltracks(len(music_id))
                return album
            
        except Exception as err:
            pass
        
        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url if instance.cover.url else None
        req['artists'] = instance.artist_id.values('id', 'name')
        req['musics'] = instance.music_id.values('id', 'title')
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['updated_at'] = instance.updated_at
        req['created_at'] = instance.created_at
        
        return req
    
    
    
    
    
    
class AddArtistToAlbums(serializers.ModelSerializer):
    """
        - Serializer for increase artist of albums
        - Based on : albums model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    artist_id = serializers.PrimaryKeyRelatedField(queryset=ArtistsModel.objects.all(), many=True)

    class Meta:
        model = AlbumModel
        fields = ['id', 'artist_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['artist_id']:
            instance.artist_id.add(i.pk)
       
        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['artists'] = instance.artist_id.values('id', 'name')
        req['updated_at'] = instance.updated_at
        
        return req




class RemoveArtistFromAlbums(serializers.ModelSerializer):
    """
        - Serializer for decrease artist of albums
        - Based on : albums model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    artist_id = serializers.PrimaryKeyRelatedField(queryset=ArtistsModel.objects.all(), many=True)

    class Meta:
        model = AlbumModel
        fields = ['id', 'artist_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        
    
        for i in validated_data['artist_id']:
            instance.artist_id.remove(i.pk)
       
        return instance

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['artists'] = instance.artist_id.values('id', 'name')
        req['updated_at'] = instance.updated_at
        
        return req

    
    
    



class AddMusicToAlbums(serializers.ModelSerializer):
    """
        - Serializer for increase music of albums
        - Based on : albums model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    music_id = serializers.PrimaryKeyRelatedField(queryset=MusicModel.objects.all(), many=True)

    class Meta:
        model = AlbumModel
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
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['musics'] = instance.music_id.values('id', 'title')
        req['totaltracks'] = instance.totaltracks
        req['updated_at'] = instance.updated_at
        
        return req




class RemoveMusicFromAlbums(serializers.ModelSerializer):
    """
        - Serializer for decrease music of albums
        - Based on : albums model
        - METHOD : PATCH
        - Relation to  artist , music , album
    """    
    music_id = serializers.PrimaryKeyRelatedField(queryset=MusicModel.objects.all(), many=True)

    class Meta:
        model = AlbumModel
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
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['musics'] = instance.music_id.values('id', 'title')
        req['totaltracks'] = instance.totaltracks
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
        fields = ['id', 'title', 'cover', 'description']
        read_only_fields = ['id',]
        
    def update(self, instance, validated_data):
        try:
         
            for attr , value in validated_data.items():
                setattr(instance, attr, value)
                
            instance.save()
            
            return instance
        
        except Exception as err:
            pass

        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url if instance.cover.url else None
        req['description'] = instance.description
        req['updated_at'] = instance.updated_at
        req['created_at'] = instance.created_at
        
        
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
        
  
            
        req['id'] = instance.pk
        req['title'] = instance.title
        req['cover'] = instance.cover.url if instance.cover.url else None
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['artists'] = instance.artist_id.values('id', 'name', 'image')
        req['musics'] = [ {'id': music.id, 'title': music.title, 'file': music.file.url, 'cover':music.cover.url, 'duration': music.duration,  'artist' : [{'id': artist.id , 'name': artist.name, 'image': artist.image.url, 'bio': artist.bio} for artist in music.artist_id.all()]} for music in instance.music_id.all()]
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        
        return req
    
    
    