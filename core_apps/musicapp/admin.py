from django.contrib import admin


from .models.playlists import PlaylistModel
from .models.musics import MusicModel


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
    
    
    

admin.site.register(PlaylistModel, PlaylistSite)
admin.site.register(MusicModel, MusicSite)