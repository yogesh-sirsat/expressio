from django.contrib import admin
from . import models


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'author', 'title', 'status', 'published')
    prepopulated_fields = {'slug': ('title',), }


admin.site.register(models.Profile)
admin.site.register(models.Category)
admin.site.register(models.Post, PostAdmin)
