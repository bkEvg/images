from django.contrib import admin
from .models import Image, ConvertedImage


class ConvertedImageAdmin(admin.TabularInline):
    model = ConvertedImage


class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [ConvertedImageAdmin]


admin.site.register(Image, ImageAdmin)



