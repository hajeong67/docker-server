# Register your models here.
from django.contrib import admin
from .models import Wheel, WatchData

@admin.register(WatchData)
class WatchDataAdmin(admin.ModelAdmin):
    list_display = ('uuid',"name",'is_active','ppg_data','imu_data','created_at',)
    list_filter = ('is_active','created_at')
    search_fields = ('uuid', 'name')
    fieldsets = (
            ("INFO", {
                "fields": ["uuid","is_active","name","created_at",]
            }),
            ("DATA", {
                "fields": ["ppg_data","imu_data"]
            })
    )

@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    list_display = ('name','version','created_at')