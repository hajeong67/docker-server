import time

from django.db import models
from pypackages.parsers.metadata import WheelMetadata

# class WatchData(models.Model):
#    uuid = models.UUIDField(unique=True)
#    name = models.CharField(max_length=20)
#    is_active = models.BooleanField(default=False)
#    ppg_data = models.JSONField() # 리스트 저장
#    imu_data = models.JSONField()
#    created_at = models.DateTimeField(blank=True, null=True)
#
#    def __str__(self):
#        return self.name

def learning_data_path(instance, filename):
    name = filename.split('-')[0]
    return f'wheels/{name}/{int(time.time())}_{filename}'

class Wheel(models.Model):
    name = models.CharField(max_length=20)
    version = models.CharField( max_length=20)
    whl_file = models.FileField(upload_to=learning_data_path, blank=True, null=True)
    #author = models.ForeignKey(WatchData,on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    license = models.CharField(max_length=50, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.version}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        wheel_meta = WheelMetadata(self.whl_file.path)

        self.name = wheel_meta.get_name()
        self.version = wheel_meta.get_version()
        self.license = wheel_meta.get_license()
        self.summary = wheel_meta.get_summary()
        self.keywords = wheel_meta.get_keywords()

        super().save()