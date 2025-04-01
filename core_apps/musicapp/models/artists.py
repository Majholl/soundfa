from django.db import models
from time import time
from os import path


"""
    -This file is include all fields for the artists models 

    ## ArtistsModels class which have all the fields needed
    ## artists_direcrory function which save the given file in the defined storage

"""



def artists_direcrory(instance , filename): 
    try:
        splitedName = path.splitext(filename) 
        fileName = f'{instance.name}_{instance.updated_at}{splitedName[-1]}'
        return path.join('artists', fileName)
    except Exception as err :
        print(f'Error while editing artist img name : error {str(err)}')


def nowTimeStamp():
    return int(time())


class ArtistsModels(models.Model):
    
    name = models.CharField(max_length=32)
    realname = models.CharField(max_length=64, null=True)
    
    bio = models.CharField(max_length=256, null=True)
    image = models.ImageField(upload_to=artists_direcrory)
    
    created_at = models.BigIntegerField(default=nowTimeStamp)
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    class Meta:
        db_table = 'artists'