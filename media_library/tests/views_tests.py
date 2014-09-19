"""Tests for the views of the ``media_library`` app."""
from django.test import TestCase
from django.core.urlresolvers import reverse

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from user_media.tests.factories import UserMediaImageFactory

from .. import models
from . import factories
from .. import views


# Test Mixins =================================================================

class MediaItemImageCRUDViewTestMixin(ViewRequestFactoryTestMixin):

    def get_view_kwargs(self):
        return {'image_pk': self.image.pk}

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.library = factories.MediaLibraryFactory(user=self.user)
        self.image = UserMediaImageFactory(
            user=self.user, content_object=self.library,
        )
        self.data = {
            'location': u'Berlin',
        }

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_callable(user=self.user)
        self.is_postable(
            user=self.user, data=self.data, to=reverse('medialibrary_edit'),
        )

        if hasattr(self, 'mediaitem'):
            self.is_not_callable(user=self.other_user)


class MediaItemVideoCRUDViewTestMixin(ViewRequestFactoryTestMixin):

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.library = factories.MediaLibraryFactory(user=self.user)
        self.data = {
            'location': u'Berlin',
            'video': u'https://youtube.com/watch?v=123456',
        }

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_callable(user=self.user)
        self.is_postable(
            user=self.user, data=self.data, to=reverse('medialibrary_edit'),
        )
        if hasattr(self, 'mediaitem'):
            self.is_not_callable(user=self.other_user)


# Tests =======================================================================

class MediaLibraryEditViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``MediaLibraryEditView`` view class."""
    view_class = views.MediaLibraryEditView

    def setUp(self):
        self.user = UserFactory()

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_callable(user=self.user)


class MediaItemDeleteViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``MediaItemDeleteView`` view class."""
    view_class = views.MediaItemDeleteView

    def get_view_kwargs(self):
        return {'pk': self.mediaitem.pk}

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.mediaitem = factories.MediaItemFactory(
            image=UserMediaImageFactory(),
            library__user=self.user)

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_callable(user=self.user)
        self.is_not_callable(user=self.other_user)
        self.is_postable(user=self.user, data={}, to=reverse(
            'medialibrary_edit'))
        self.assertEqual(models.MediaItem.objects.count(), 0, msg=(
            'The media item should be deleted.'
        ))


class MediaItemImageCreateViewTestCase(MediaItemImageCRUDViewTestMixin,
                                       TestCase):
    """Tests for the ``MediaItemImageCreateView`` view class."""
    view_class = views.MediaItemImageCreateView


class MediaItemImageUpdateViewTestCase(MediaItemImageCRUDViewTestMixin,
                                       TestCase):
    """Tests for the ``MediaItemImageUpdateView`` view class."""
    view_class = views.MediaItemImageUpdateView

    def setUp(self):
        super(MediaItemImageUpdateViewTestCase, self).setUp()
        self.mediaitem = factories.MediaItemFactory(
            image=self.image, library=self.library,
        )


class MediaItemVideoCreateViewTestCase(MediaItemVideoCRUDViewTestMixin,
                                       TestCase):
    """Tests for the ``MediaItemVideoCreateView`` view class."""
    view_class = views.MediaItemVideoCreateView


class MediaItemVideoUpdateViewTestCase(MediaItemVideoCRUDViewTestMixin,
                                       TestCase):
    """Tests for the ``MediaItemVideoUpdateView`` view class."""
    view_class = views.MediaItemVideoUpdateView

    def get_view_kwargs(self):
        return {'pk': self.mediaitem.pk}

    def setUp(self):
        super(MediaItemVideoUpdateViewTestCase, self).setUp()
        self.mediaitem = factories.MediaItemFactory(
            library=self.library, user=self.user,
        )


class MediaLibraryUploadViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``MediaLibraryUploadView`` view class."""
    view_class = views.MediaLibraryUploadView

    def setUp(self):
        self.user = UserFactory()
        self.library = factories.MediaLibraryFactory(user=self.user)

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_callable(user=self.user)
        self.assertEqual(models.MediaLibrary.objects.count(), 1, msg=(
            'There should be one media item automatically created.'
        ))
