from django.db import models

from time import time
from os import path
from loguru import logger

# -------------------------------------------------------------------
    ### Artist Model ###

# This model adds artists :
# - Many-to-many relationship with artist, musics, albums , generes
# - Timestamp fields for creation and last update

# -------------------------------------------------------------------



def artists_direcrory(instance , filename): 
    try:
        splitedName = path.splitext(filename) 
        fileName = f'{instance.name}_{int(time())}{splitedName[-1]}'
        return path.join('artists', fileName)
    except Exception as err :
        logger.info(f'Error saving artist  image name | artist-id : {instance.pk} | {str(err)}')
        print(f'Error saving artist image name | artist-id : {instance.pk} | {str(err)}')



class ArtistsModel(models.Model):
    
    name = models.CharField('Artist name', max_length=32)
    realname = models.CharField('Artist realname', max_length=64, null=True)
    bio = models.CharField('Artist bio', max_length=256, null=True)
    image = models.ImageField(verbose_name='Artist image', upload_to=artists_direcrory)
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)

    
    class Meta:
        verbose_name = 'Artist'
        db_table = 'artists'
        ordering = ['-name']


    def __str__(self):
        return f'{self.name}'