from django.urls import path
from .views import view_artists , view_musics , view_albums , view_genres, view_playlists

artist_url = [
    path('artist/add/' , view_artists.add_artist, name='Artist-add'),
    path('artist/update/', view_artists.update_artist , name='Artist-update'),
    path('artist/artists/', view_artists.get_all_artists , name='Artists-list'),
    path('artist/', view_artists.get_one_artist, name='Aritst-one'),
    path('artist/<str:name>', view_artists.get_one_artist, name='Aritst-one'),
    path('artist/delete/' , view_artists.delete_artist , name='Artist-deletion'),
]



music_url = [
    path('music/add', view_musics.add_music, name='Music-add'),
    path('music/update/', view_musics.update_music, name='Music-update'),
    path('music/', view_musics.get_music_by_musicname, name='Music-by-music-name'),
    path('music/<str:name>', view_musics.get_music_by_musicname, name='Music-by-music-name'),
    path('music/artist/', view_musics.get_music_by_artistname, name='Music-by-artist-name'),
    path('music/artist/<str:name>', view_musics.get_music_by_artistname, name='Music-by-artist-name'),
    path('music/delete/', view_musics.delete_music, name='Music-delete'),
    path('music/download/music/<str:filename>', view_musics.download_music, name='download-music'),
]



album_url = [
    path('album/add/', view_albums.add_album, name='Album-add'),
    path('album/update/', view_albums.update_album, name='Album-update'),
    path('album/albums/', view_albums.get_all_albums, name='Albums-list'),
    path('album/', view_albums.get_album_by_album_name, name='Album-by-Album-name'),
    path('album/<str:title>/', view_albums.get_album_by_album_name, name='Album-by-Album-name'),
    path('album/delete/', view_albums.delete_album, name='Album-delete'), 
]




genere_url = [
    path('genere/add/', view_genres.add_genere, name='Genere-add'),
    path('genere/', view_genres.get_all_genere, name='All-generes'),
    path('genere/genere/', view_genres.get_genere, name='Get-generes'),
    path('genere/delete/', view_genres.delete_genere, name='Genere-delete'),
]



playlist_url = [
    path('playlist/add/', view_playlists.add_playlist, name='Playlsit-add'),
    path('playlist/update/', view_playlists.update_playlist, name='Playlist-update'),
    path('playlist/playlists/', view_playlists.get_all_playlist_user, name='All-playlists'),
    path('playlist/', view_playlists.get_playlist_user, name='get-playlists'),
    path('playlist/delete/', view_playlists.delete_playlist, name='Playlsit-delete'),
]


urlpatterns = artist_url + music_url + album_url + genere_url + playlist_url