"""Tests for the models of the ``media_library`` app."""
from django.test import TestCase

from user_media.models import UserMediaImage
from user_media.tests.factories import UserMediaImageFactory

from . import factories


class MediaLibraryTestCase(TestCase):
    """Tests for the ``MediaLibrary`` model class."""
    longMessage = True

    def test_instantiation(self):
        library = factories.MediaLibraryFactory()
        self.assertTrue(library.pk)


class MediaItemTestCase(TestCase):
    """Tests for the ``MediaItem`` model class."""
    longMessage = True

    def assertNotRaises(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            self.fail(msg=(
                '"{0}" should not have raised an exception, but raised'
                ' "{1}"'.format(repr(func), str(ex))
            ))

    def setUp(self):
        self.library = factories.MediaLibraryFactory()
        self.mediaitem = factories.MediaItemFactory(
            showreel=self.library,
            video='https://youtube.com/watch?v=123456',
        )
        self.umedia_image = UserMediaImageFactory()
        self.mediaitemimage = factories.MediaItemFactory(
            video=None, image=self.umedia_image,
        )

    def test_delete(self):
        self.mediaitemimage.delete()
        self.assertEqual(UserMediaImage.objects.count(), 0, msg=(
            'The user media images should have been deleted as well.'
        ))

    def test_instantiation(self):
        self.assertTrue(self.mediaitem.pk)

    def test_video_id(self):
        self.assertEqual(self.mediaitem.video_id, '123456', msg=(
            'The property should have returned the correct video id.'
        ))

    def test_clean(self):
        linklist = [
            'http://www.youtube.com/watch?v=-JyZLS2IhkQ',
            'https://www.youtube.com/watch?v=-JyZLS2IhkQ',
            'http://www.youtube.de/watch?v=-JyZLS2IhkQ',
            'https://youtube.com/watch?v=-JyZLS2IhkQ',
            ('https://www.youtube.com/watch?v=PguLNvCcOHQ'
             '&list=RDPguLNvCcOHQ#t=0'),
            'http://youtu.be/PguLNvCcOHQ?list=RDPguLNvCcOHQ ',
            'http://vimeo.com/channels/staffpicks/110140870',
            'http://vimeo.com/59777392',
            'http://vimeo.com/video/59777392',
            ('http://vimeo.com/groups/thedirectorofphotography/'
             'videos/110016243'),
        ]
        for link in linklist:
            self.mediaitem.video = link
            self.assertNotRaises(self.mediaitem.clean)
