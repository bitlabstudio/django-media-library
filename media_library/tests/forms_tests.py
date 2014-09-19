"""Tests for the forms of the ``media_library`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from user_media.tests.factories import UserMediaImageFactory
from multilingual_tags.models import Tag, TaggedItem

from . import factories
from .. import forms, models


class MediaItemImageFormTestCase(TestCase):
    """Tests for the ``MediaItemImageForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.library = factories.MediaLibraryFactory(user=self.user)
        self.image = UserMediaImageFactory(
            user=self.user, content_object=self.library)
        self.data = {
            'location': u'Berlin',
            'date': u'12/12/2012',
            'tags': u'foo, bar, foobar'
        }
        self.data_update = {
            'location': u'Hamburg',
        }

    def test_form(self):
        form = forms.MediaItemImageForm(
            data=self.data, user=self.user, image=self.image,
        )
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        instance = form.save()
        self.assertEqual(models.MediaItem.objects.count(), 1, msg=(
            'The form should have created one MediaItem.'
        ))
        self.assertEqual(Tag.objects.count(), 3, msg=(
            'The form should have created 3 tags.'
        ))
        self.assertEqual(TaggedItem.objects.count(), 3, msg=(
            'The form should have created 3 tagged items.'
        ))

        form = forms.MediaItemImageForm(
            data=self.data_update, user=self.user, image=self.image,
            instance=instance,
        )
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        instance = form.save()
        self.assertEqual(models.MediaItem.objects.count(), 1, msg=(
            'There should still be only one MediaItem.'
        ))
        self.assertEqual(Tag.objects.count(), 3, msg=(
            'There should still be only 3 tags'
        ))
        self.assertEqual(TaggedItem.objects.count(), 3, msg=(
            'There should still be only 3 tagged items.'
        ))
        self.assertEqual(instance.location, 'Hamburg', msg=(
            'The form should have updated the location field.'
        ))


class MediaItemVideoFormTestCase(TestCase):
    """Tests for the ``MediaItemVideoForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.library = factories.MediaLibraryFactory(user=self.user)
        self.data = {
            'video': u'https://youtube.com/watch?v=123456',
            'location': u'Berlin',
            'date': u'12/12/2012',
            'tags': u'foo, bar, foobar'
        }
        self.data_update = {
            'location': u'Hamburg',
        }

    def test_form(self):
        form = forms.MediaItemVideoForm(data=self.data, user=self.user)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        instance = form.save()
        self.assertEqual(models.MediaItem.objects.count(), 1, msg=(
            'The form should have created one MediaItem.'
        ))

        form = forms.MediaItemVideoForm(
            data=self.data_update, user=self.user, instance=instance,
        )
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(models.MediaItem.objects.count(), 1, msg=(
            'There should still be only one MediaItem.'
        ))
