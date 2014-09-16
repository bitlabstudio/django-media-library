"""Factories for the models of the ``media_library`` app."""
import factory
from django_libs.tests.factories import HvadFactoryMixin, UserFactory

from media_library import models


class MediaLibraryFactory(factory.DjangoModelFactory):
    """Factory for the ``MediaLibrary`` model class."""
    FACTORY_FOR = models.MediaLibrary

    user = factory.SubFactory(UserFactory)


class MediaItemFactory(HvadFactoryMixin, factory.DjangoModelFactory):
    """Factory for the ``MediaItem`` model class."""
    FACTORY_FOR = models.MediaItem

    library = factory.SubFactory(MediaLibraryFactory)
    video = 'https://youtube.com/watch?v=123456'

    language_code = 'en'
