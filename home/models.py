from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    telegram = models.URLField()
    tlgactive = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    limitcount = models.DecimalField(default=100,max_digits=5, decimal_places=1)

class CoinData(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField()    
    created_on = models.DateTimeField(unique=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        super(CoinData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['created_on']
class VolumeData(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField()    
    created_on = models.DateTimeField(unique=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        super(VolumeData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['created_on']

class CandleData(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField()    
    created_on = models.DateTimeField(unique=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        super(CandleData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['created_on']
class CandleHourData(models.Model):
    id = models.AutoField(primary_key=True)
    coin_id = models.IntegerField()
    data = models.TextField()    
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(CandleHourData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['created_on']
       
class UserSettingsData(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    data = models.TextField()

    def save(self, *args, **kwargs):
        super(UserSettingsData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['userid']  
class UserNotifyData(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    data = models.TextField()
    status = models.TextField()
    def save(self, *args, **kwargs):
        super(UserNotifyData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['userid'] 
    
