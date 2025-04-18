from rest_framework import serializers
from ..models.albums import AlbumModel


class GetAllListsSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = AlbumModel
        fields = ['id', 'title', 'albumcover', 'music_id', 'totaltracks', 'description']
        read_only_fields =['id']
        
    def to_representation(self, instance):
        req = {}
        req['id'] = instance.pk
        req['title'] = instance.title
        req['albumcover'] = instance.albumcover.url
        req['musics'] = instance.music_id.values('id', 'title', 'musiccover', 'musicfile')
        req['totaltracks'] = instance.totaltracks
        req['description'] = instance.description
        req['created_at'] = instance.created_at
        req['updated_at'] = instance.updated_at
        
        return req
    
    
    