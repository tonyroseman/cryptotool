from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
# Create your models here.
class CustomUser(AbstractUser):
    telegram = models.URLField(default="", blank=True)
    tlgactive = models.DecimalField(default=0,max_digits=10, decimal_places=0)
    phone = models.CharField(default="", blank=True,max_length=20)
    limitcount = models.DecimalField(default=500,max_digits=5, decimal_places=0)
    is_login = models.DecimalField(default=0,max_digits=10, decimal_places=0)
    # expired_time = models.DateField(default=timezone.now() + timezone.timedelta(days=365))
    expired_time = models.DateTimeField(default=datetime.datetime(2023, 12, 31, 23, 59, 59))

class CoinData(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.TextField(default="")
    data = models.TextField()    
    created_on = models.DateTimeField(unique=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        super(CoinData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['id']


class UserSettingsData(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    data = models.TextField()

    def save(self, *args, **kwargs):
        super(UserSettingsData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['userid']
class UserAdvancedSettingsData(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    data = models.TextField()

    def save(self, *args, **kwargs):
        super(UserAdvancedSettingsData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['userid']  
class SystemSettingsData(models.Model):
    id = models.AutoField(primary_key=True)
    
    data = models.TextField()

    def save(self, *args, **kwargs):
        super(SystemSettingsData, self).save(*args, **kwargs)
    
class UserNotifyData(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    data = models.TextField()
    created_on = models.DateTimeField(unique=False, auto_now_add=True)
    def save(self, *args, **kwargs):
        super(UserNotifyData, self).save(*args, **kwargs)
    class Meta:
        ordering = ['id'] 
class ErrorLog(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField()    
    data = models.TextField()
    type = models.TextField()
    created_on = models.DateTimeField(unique=False, auto_now_add=True)
    def save(self, *args, **kwargs):
        super(ErrorLog, self).save(*args, **kwargs)
    class Meta:
        ordering = ['-created_on'] 
class TelegramList(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField()
    created_on = models.DateTimeField(unique=False, auto_now_add=True)
    def save(self, *args, **kwargs):
        super(TelegramList, self).save(*args, **kwargs)
    
    
