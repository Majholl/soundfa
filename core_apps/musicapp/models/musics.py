from django.db import models
from time import time
from os import path
from loguru import logger

from .artists import ArtistsModel


# -------------------------------------------------------------------
    ### Music Model ###

# This model adds music for artists or non-artist:
# - Many-to-many relationship with artist
# - Timestamp fields for creation and last update

# -------------------------------------------------------------------



def music_file_cover(instance, filename):
    try:
        
        splitedName = path.splitext(filename)
        fileName = f'{instance.title}_{int(time())}{splitedName[-1]}'
        return path.join('musics', fileName)
    
    except Exception as err:
        logger.info(f'Error saving music cover image name | music-id : {instance.pk} | {str(err)}')
        print(f'Error saving music cover image name | music-id : {instance.pk} | {str(err)}')




class MusicModel(models.Model):
    
    title = models.CharField('Music title', max_length=32)
    duration = models.CharField('Music duration', max_length=32, null=True)
    lyrics = models.TextField('Music lyrics', null=True)
    
    artist_id = models.ManyToManyField(verbose_name='Artists', to=ArtistsModel, related_name='artist_id')
    
    cover = models.ImageField('Music cover', upload_to=music_file_cover)
    file = models.FileField('Music file', upload_to=music_file_cover)
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)
    
    class Meta:
        verbose_name = 'Music'
        db_table = 'musics'
        ordering = ['-title']
        
    def __str__(self):
        return f'{self.title}'