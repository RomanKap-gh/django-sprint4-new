from django.contrib import admin

from .models import Category, Location, Post, Comment

import core.constants as constants


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'created_at',
        'is_published',
        'author',
        'category',
        'location'
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)

    empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'post',
        'text_preview',
        'created_at'
    )

    def text_preview(self, obj):
        if len(obj.text) <= constants.SHORT_TEXT_SIZE:
            return obj.text
        return f'{obj.text[:constants.SHORT_TEXT_SIZE]}...'


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
