"""Models for the ``media_library`` app."""
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hvad.models import TranslatableModel, TranslatedFields

from .utils import get_video_id, validate_video_url


class MediaLibrary(models.Model):
    """
    General collection of ``MediaItem`` objects for a user.

    :user: FK to the ``User`` object this collection belongs to.
    :user_media_images: a generic relation to user media images of this user

    """

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('user'),
        related_name='medialibraries',
    )

    user_media_images = generic.GenericRelation(
        'user_media.UserMediaImage',
    )

    def __unicode__(self):
        return 'Library of "{0}"'.format(self.user.email)

    def get_absolute_url(self):
        return reverse('showreel_edit')


class MediaItem(TranslatableModel):
    """
    Stores video URLs and references ``UserMediaImage`` and extends them with
    some additional meta data.

    :library: the library this item belongs to.
    :image: FK to a ``UserMediaImage``. Optional.
    :video: URL of a youtube video. Optional
    :date: The date this video or image was taken.
    :tags: A generic relation to the ``TaggedItem`` from ``multilingual_tags``.
    :generic_position: A generic relation to ``ObjectPosition``.

    translatable:
    :location: The place where this image or video was taken

    """

    library = models.ForeignKey(
        MediaLibrary,
        verbose_name=_('library'),
        related_name='media_items',
    )

    image = models.ForeignKey(
        'user_media.UserMediaImage',
        verbose_name=_('image'),
        related_name='media_items',
        blank=True, null=True,
    )

    video = models.URLField(
        verbose_name=_('video'),
        help_text=_('Enter a YouTube or Vimeo video URL here.'),
        max_length=512,
        blank=True, null=True,
    )

    date = models.DateField(
        verbose_name=_('date'),
        blank=True, null=True,
    )

    translations = TranslatedFields(
        location=models.CharField(
            verbose_name=_('location'),
            max_length=256,
            blank=True,
        )
    )

    tags = generic.GenericRelation(
        'multilingual_tags.TaggedItem',
    )

    generic_position = generic.GenericRelation(
        'generic_positions.ObjectPosition',
    )

    def __unicode__(self):
        if self.image is not None:
            return 'Image of "{0}"'.format(self.library.user)
        return 'Video of "{0}"'.format(self.library.user)

    def clean(self):
        """
        Checks if the video has the correct format.

        Currently supported are vimeo and youtube.

        """
        if self.video and self.get_video_origin() is None:
            raise ValidationError(_(
                'The video URL was not in a valid Vimeo or YouTube format.'
            ))

    def get_video_origin(self):
        return validate_video_url(self.video)

    def get_user(self):
        """Returns a user for the ``django-multilingual-tags`` form API."""
        return self.library.user

    def delete(self, using=None):
        # making sure, the UserMediaImage instance is removed as well.
        if self.image is not None:
            self.image.delete()
        super(MediaItem, self).delete(using=using)

    @property
    def video_id(self):
        """Returns the video ID from the URL."""
        return get_video_id(self.video)
