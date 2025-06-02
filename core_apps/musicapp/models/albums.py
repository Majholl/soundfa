from django.db import models

from time import time
from os import path
from loguru import logger

from .artists import ArtistsModel
from .musics import MusicModel


# -------------------------------------------------------------------
    ### Album Model ###

# This model adds artists :
# - Many-to-many relationship with artist, musics
# - Timestamp fields for creation and last update

# -------------------------------------------------------------------



def album_file_cover(instance ,filename):
    try:
        splitedName = path.splitext(filename)
        fileName = f'{instance.title}_{int(time())}{splitedName[-1]}'
        return path.join('albums', fileName)
    except Exception as err:
        logger.info(f'Error saving artist  image name | artist-id : {instance.pk} | {str(err)}')
        print(f'Error saving artist image name | artist-id : {instance.pk} | {str(err)}')




class AlbumModel(models.Model):
    
    title = models.CharField('Album title', max_length=32)
    cover = models.FileField(verbose_name='Album cover', upload_to=album_file_cover)

    artist_id = models.ManyToManyField(verbose_name='Artists ablbum', to=ArtistsModel, blank=True)
    music_id = models.ManyToManyField(verbose_name='Musics ablbum',to=MusicModel, blank=True)
    
    totaltracks = models.BigIntegerField('Ablum totaltracks', null=True, blank=True)
    description = models.CharField('Album description', max_length=256, null=True)
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)

    class Meta :
        verbose_name = 'Albums'
        db_table = 'albums'
        ordering = ['-title']
        
    def count_totaltracks(self, count):
        self.totaltracks = count
        self.save()    
        
    def __str__(self):
        return f'{self.title}'        