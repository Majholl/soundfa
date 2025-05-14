from django.contrib import admin


from .models.playlists import PlaylistModel
from .models.musics import MusicModel


class PlaylisySite(admin.ModelAdmin):
    list_display = ['title', 'description', 'cover', 'totaltracks', 'public_playlist']
    
    list_display_links = ['title', 'description']
    
    list_per_page = 15
    
    search_fields = ['playlists__title', 'playlists__public_playlist']
    
    list_filter = ['title', 'public_playlist']
    
    readonly_fields = ('get_musics_data',)
    
    fieldsets = (
            
            ('Playlist info', {
                'fields': ('title', 'description')
            }),
            
            ('others', {
                'fields': ('cover', 'totaltracks', 'public_playlist'),
            }),
            
            ('musics', {
                'fields': ('get_musics_data', 'music_id'),
            }),
            
        )
    def get_musics_data(self, obj):
        return ','.join([f" {i.pk}-{i.title} " for i in obj.music_id.all()])
    
    get_musics_data.short_description = 'musics - data'
    
    
admin.site.register(PlaylistModel, PlaylisySite)
admin.site.register(MusicModel)