"""Admins for the models of the ``media_library`` app."""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class MediaItemAdmin(admin.ModelAdmin):
    """Custom admin for the ``MediaItem`` model."""
    list_display = ['get_user', 'image', 'video']

    def get_user(self, obj):
        return obj.library.user
    get_user.short_description = _('user')


admin.site.register(models.MediaLibrary)
admin.site.register(models.MediaItem, MediaItemAdmin)
