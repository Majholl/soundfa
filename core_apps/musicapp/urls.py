from django.urls import path
from .views import view_artists , view_musics , view_albums

artist_url = [
    path('artist/add/' , view_artists.add_artist, name='Artist-add'),
    path('artist/update/', view_artists.update_artist , name='Artist-update'),
    path('artist/artists/', view_artists.get_all_artists , name='Artist-lists'),
    path('artist/', view_artists.get_one_artist, name='Aritst-one'),
    path('artist/<str:name>', view_artists.get_one_artist, name='Aritst-one'),
    path('artist/delete/' , view_artists.delete_artist , name='Artist-deletion'),
]



music_url = [
    path('music/add', view_musics.add_music, name='Music-add'),
    path('music/update', view_musics.update_music, name='Music-update'),
    path('music/', view_musics.get_music_by_musicname, name='Music-by-music-name'),
    path('music/<str:name>', view_musics.get_music_by_musicname, name='Music-by-music-name'),
    path('music/artist/', view_musics.get_music_by_artistname, name='Music-by-artist-name'),
    path('music/artist/<str:name>', view_musics.get_music_by_artistname, name='Music-by-artist-name'),
    path('music/delete/', view_musics.delete_music, name='Music-delete'),
    path('music/download/music/<str:filename>', view_musics.download_music, name='download-music'),
]



albuom_url = [
    path('album/add', view_albums.add_album, name='Album-add'),
    path('album/update', view_albums.update_album, name='Album-update'),
    path('album/', view_albums.get_album_by_album_name, name='Album-by-Album-name'),
    path('album/<str:title>/', view_albums.get_album_by_album_name, name='Album-by-Album-name'),
    path('album/delete/', view_albums.delete_album, name='Album-delete'), 
]


urlpatterns = artist_url + music_url + albuom_url