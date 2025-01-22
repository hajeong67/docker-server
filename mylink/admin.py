from django.contrib import admin
from .models import Category, Link, Tag, LinkTag

class LinkTagInline(admin.TabularInline):
    model = LinkTag
    extra = 1

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name')  # ForeignKey 필드는 __name으로 검색
    inlines = [LinkTagInline]

    fieldsets = (
        ("Basic Information", {
            "fields": ["name", "url", "thumbnail", "note"]
        }),
        ("Category", {
            "fields": ["category"]
        }),
        ("Timestamps", {
            "fields": ["created_at", "updated_at"],
            "classes": ["collapse"]
        }),
    )

    readonly_fields = ("created_at", "updated_at")  # 읽기 전용

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)