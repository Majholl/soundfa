from django.urls import path
from .views import view_artists , view_musics , view_albums , view_genres, view_playlists



music_url = [
    path('music/add/', view_musics.add_music, name='Music-add'),
    path('music/delete/<int:id>', view_musics.delete_music, name='Music-delete'), 
    path('music/update/', view_musics.update_music, name='Music-update'),
    path('music/musics', view_musics.get_all_musics, name='Music-all-musics'),
    path('music/music-artist-search/', view_musics.search_in_musics_artists, name='Music-artist-searching'),
    path('music/musics/<str:qset>/', view_musics.get_music_by_musicname, name='Music-music-name'),
    path('music/artist/<str:qset>/', view_musics.get_music_by_artistname, name='Music-artist-name'),
    path('music/download/music/<str:filename>', view_musics.download_music, name='download-music'),
]





playlist_url = [
    path('playlist/add/', view_playlists.add_playlist, name='Playlist-add'),
    path('playlist/delete/<int:id>', view_playlists.delete_playlist, name='Playlist-delete'),
    path('playlist/addmusic/', view_playlists.add_music_to_playlist, name='Add-music-to-playlist'),
    path('playlist/removemusic/', view_playlists.remove_music_to_playlist, name='Remove-music-from-playlist'),
    path('playlist/<int:id>', view_playlists.get_playlist_user, name='get-user-playlists'),
    path('playlist/playlists/', view_playlists.get_all_playlists_user, name='All-user-playlists'),
    path('playlist/public/', view_playlists.get_all_public_playlist, name='All-public-playlists'),
    path('playlist/update/', view_playlists.update_playlist, name='Playlist-update'),
]




genere_url = [
    path('genere/add/', view_genres.add_genere, name='Genere-add'),
    path('genere/delete/<int:id>', view_genres.delete_genere, name='Genere-delete'),
    
    path('genere/addartist/', view_genres.add_artist_to_genere, name='Add-artist-to-genere'),
    path('genere/removeartist/', view_genres.remove_artist_from_genere, name='Remove-artist-to-genere'),
    
    
    path('genere/update/', view_genres.update_genere, name='Genere-update'),
    path('genere/', view_genres.get_all_genere, name='All-generes'),
    path('genere/generes/', view_genres.get_genere, name='Get-generes'),
]












album_url = [
    path('album/add/', view_albums.add_album, name='Album-add'),
    path('album/update/', view_albums.update_album, name='Album-update'),
    path('album/albums/', view_albums.get_all_albums, name='Albums-list'),
    path('album/', view_albums.get_album_by_album_name, name='Album-by-Album-name'),
    path('album/<str:title>/', view_albums.get_album_by_album_name, name='Album-by-Album-name'),
    path('album/delete/', view_albums.delete_album, name='Album-delete'), 
    
]


artist_url = [
    path('artist/add/' , view_artists.add_artist, name='Artist-add'),
    path('artist/update/', view_artists.update_artist , name='Artist-update'),
    path('artist/artists/', view_artists.get_all_artists , name='Artists-list'),
    path('artist/', view_artists.get_one_artist, name='Aritst-one'),
    path('artist/<str:name>', view_artists.get_one_artist, name='Aritst-one'),
    path('artist/delete/' , view_artists.delete_artist , name='Artist-deletion'),
]


urlpatterns = artist_url + music_url + album_url + genere_url + playlist_url