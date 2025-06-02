from django.contrib import admin


from .models.playlists import PlaylistModel
from .models.musics import MusicModel
from .models.artists import ArtistsModel
from .models.albums import AlbumModel
from .models.genres import GenereModel



class PlaylistSite(admin.ModelAdmin):
    list_display = ['title', 'description', 'cover', 'totaltracks', 'public_playlist']
    
    list_display_links = ['title', 'description']
    
    list_per_page = 15
    
    search_fields = ['playlists__title', 'playlists__public_playlist']
    
    list_filter = ['title', 'public_playlist']
    
    readonly_fields = ('get_musics_data', 'created_at', 'updated_at')
    
    fieldsets = (
            
            ('Playlist info', {
                'fields': ('title', 'description',)
            }),
            
            ('Others', {
                'fields': ('cover', 'totaltracks', 'public_playlist',),
            }),
            
            ('Musics', {
                'fields': ('get_musics_data', 'music_id',),
            }),
            
            ('DateTime', {'fields': ('created_at', 'updated_at',),}),
        )
    def get_musics_data(self, obj):
        return ','.join([f" {i.pk}-{i.title} " for i in obj.music_id.all()])
    
    get_musics_data.short_description = 'musics - data'
    
    
    
    
class MusicSite(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    
    list_display_links = list_display
    
    list_per_page = 15
    
    search_fields = ['musics__title', 'musics__artist_id__name']
    
    list_filter =  ['title', 'artist_id__name']
    
    readonly_fields = ('get_artists_data', 'created_at', 'updated_at',)
    
    fieldsets = (
        ('Music info', {'fields': ('title', 'duration', 'lyrics',)},),
        
        ('File-Cover', {'fields': ('cover', 'file',),}),
        
        ('Others', {'fields': ('artist_id', 'get_artists_data',),}),
        
        ('DateTime', {'fields': ('created_at', 'updated_at',),}),   
    )
    
    def get_artists_data(self, obj):
        return ','.join([f" {i.pk}-{i.name} " for i in obj.artist_id.all()])
    
    get_artists_data.short_description = 'artist - data'
    
    
  

  
class ArtistSite(admin.ModelAdmin):
    list_display = ['name', 'realname', 'bio']
    
    list_display_links = list_display
    
    list_per_page = 15
    
    search_fields = ['artist__name', 'artist__realname', 'artist__bio']
    
    list_filter =  ['name', ]
    
    readonly_fields = ('get_image_artist', 'created_at', 'updated_at',)
    
    fieldsets = (
        ('Music info', {'fields': ('name', 'realname', 'bio',)},),
        
        ('File-Cover', {'fields': ('get_image_artist',),}),
        
        ('DateTime', {'fields': ('created_at', 'updated_at',),}),   
    )
      
    def get_image_artist(self, obj):
        if not obj.image :
            return None
         
        return ','.join([f"{i.name}-{i.image.url} " for i in obj])
    
    get_image_artist.short_description = 'Image'
    


  
class AlbumSite(admin.ModelAdmin):
    list_display = ['title', 'description']
    
    list_display_links = list_display
    
    list_per_page = 15
    
    search_fields = ['album__title', 'album__artist_id__name', 'album__music_id__title']
    
    list_filter =  ['title', 'artist_id__name', 'music_id__title']
    
    readonly_fields = ('created_at', 'updated_at',)
    
    fieldsets = (
        ('Music info', {'fields': ('title', 'totaltracks', 'description',)},),
        
        ('File-Cover', {'fields': ('cover', ),}),
        
        ('DateTime', {'fields': ('created_at', 'updated_at',),}),   
    )

  
  

class GenereSite(admin.ModelAdmin):
    list_display = ['name', 'description']
    
    list_display_links = list_display
    
    list_per_page = 15
    
    search_fields = ['genere__name', 'genere__artist_id__name', 'genere__playlist_id__title', 'genere__music_id__title']
    
    list_filter =  ['name', 'artist_id__name', 'music_id__title', 'playlist_id__title']
    
    readonly_fields = ('created_at', 'updated_at',)
    
    fieldsets = (
        ('Music info', {'fields': ('name',  'description',)},),
        
        ('File-Cover', {'fields': ('cover', ),}),
        
        ('DateTime', {'fields': ('created_at', 'updated_at',),}),   
    )  
    






admin.site.register(PlaylistModel, PlaylistSite)
admin.site.register(MusicModel, MusicSite)
admin.site.register(ArtistsModel, ArtistSite)
admin.site.register(AlbumModel, AlbumSite)
admin.site.register(GenereModel, GenereSite)