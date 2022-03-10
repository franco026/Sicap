from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.admin.widgets import AdminDateWidget

class User(AbstractUser):
    # Options for types of id

    typeIdentification = models.CharField(max_length=64)
    identification = models.BigIntegerField()
    genre = models.CharField(max_length=64)
    typeUser = models.CharField(max_length=64)
    address =  models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    observation = models.CharField(max_length=100)
    
    REQUIRED_FIELDS=["typeIdentification", "identification", "genre", "typeUser", "address","title","observation"]
    def saveUser(self, *args, **kwargs):
        self.typeIdentification = (self.typeIdentification).upper()
        self.genre = (self.genre).upper()
        self.typeUser = (self.typeUser).upper()
        self.address = (self.address).upper()
        self.title = (self.title).upper()
        self.observation = (self.observation).upper()
        return User(User, self).saveUser(*args, **kwargs)

        