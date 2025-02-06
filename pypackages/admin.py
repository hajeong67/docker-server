from django.contrib import admin
from django.utils.html import format_html
from .models import Author, Wheel

# @admin.register(WatchData)
# class WatchDataAdmin(admin.ModelAdmin):
#     list_display = ('uuid',"name",'is_active','ppg_data','imu_data','created_at',)
#     list_filter = ('is_active','created_at')
#     search_fields = ('uuid', 'name')
#     fieldsets = (
#             ("INFO", {
#                 "fields": ["uuid","is_active","name","created_at",]
#             }),
#             ("DATA", {
#                 "fields": ["ppg_data","imu_data"]
#             })
#     )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name','email',]
    fieldsets = (
        (
            'Author INFO', {
                'fields': [
                    'name',
                    'email',
                ]
            }
        ),
    )
    readonly_fields = ('name', 'email')

@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'author', 'summary', 'license', 'keywords', 'created_at', 'download_link')
    list_display_links = ('name', 'version', 'created_at')  # 클릭 가능 영역 확장
    fieldsets = (
        (
            'Wheel File', {
                'fields': [
                    'whl_file',
                ]
            }
        ),
        (
            'Metadata INFO', {
                'fields': [
                    'name',
                    'version',
                    'license',
                    'summary',
                    'keywords',
                    'created_at',
                ]
            }
        ),
        (
            'Auth INFO', {
                'fields': [
                    'author',
                ]
            }
        )
    )
    readonly_fields = ('name', 'version', 'author', 'summary', 'license', 'keywords', 'description', 'created_at',)

    def download_link(self, obj):
        if obj.whl_file and obj.whl_file.url:
            return format_html('<a href="{}" download>Download</a>', obj.whl_file.url)
        return "No file"

    download_link.short_description = "Download"