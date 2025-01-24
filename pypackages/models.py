import datetime

from django.db import models

class WatchData(models.Model):
   uuid = models.UUIDField(unique=True)
   name = models.CharField(max_length=20)
   is_active = models.BooleanField(default=False)
   ppg_data = models.JSONField() # 리스트 저장
   imu_data = models.JSONField()
   created_at = models.DateTimeField(blank=True, null=True)

   def __str__(self):
       return self.name

class Wheel(models.Model):
    name = models.CharField(max_length=20)
    version = models.CharField( max_length=20)
    #author = models.ForeignKey(WatchData,on_delete=models.CASCADE,)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

# class PythonPackage