"""Tests for the utils of the ``media_library`` app."""
from django.test import TestCase

from .. import utils


class GetVideoIDTestCase(TestCase):
    """Tests for the ``get_video_id`` function."""
    longMessage = True

    def test_function(self):
        self.assertEqual(utils.get_video_id('vimeo.com/12345'), '12345')
        self.assertEqual(utils.get_video_id('vimeo.com/12345/'), '12345')
        self.assertEqual(
            utils.get_video_id('vimeo.com/username/12345'), '12345')
        self.assertEqual(
            utils.get_video_id('vimeo.com/groupname/username/12345'), '12345')
        self.assertEqual(
            utils.get_video_id('youtube.com/watch?v=12345'), '12345')
        self.assertEqual(
            utils.get_video_id('youtube.com/watch?v=12345&list=abcd#t=21'),
            '12345')


class ValidateVideoURLTestCase(TestCase):
    """Tests for the ``validate_video_url`` function."""

    def test_function(self):
        self.yt_links = [
            'http://www.youtube.com/watch?v=-JyZLS2IhkQ',
            'https://www.youtube.com/watch?v=-JyZLS2IhkQ',
            'http://www.youtube.de/watch?v=-JyZLS2IhkQ&list=foo',
            'http://www.youtube.de/watch?v=-JyZLS2IhkQ',
            'https://youtube.com/watch?v=-JyZLS2IhkQ',
            ('https://www.youtube.com/watch?v=PguLNvCcOHQ'
             '&list=RDPguLNvCcOHQ#t=0'),
            'http://youtu.be/PguLNvCcOHQ',
            'http://youtu.be/PguLNvCcOHQ?list=RDPguLNvCcOHQ',
        ]
        self.vm_links = [
            'http://vimeo.com/channels/staffpicks/110140870',
            'http://vimeo.com/59777392',
            'http://vimeopro.com/foo/bar/110140870',
            'http://vimeo.com/video/59777392',
            'http://www.vimeo.com/video/59777392',
            ('http://vimeo.com/groups/thedirectorofphotography/'
             'videos/110016243'),
        ]
        self.invalid_links = [
            'http://vimeo.com/',
            'http://vimeo.com/groups/thedirectorofphotography/',
            'http://vimeo.com/channels/staffpicks/',
            'http://www.youtube.de/watch?v=',
            'https://www.youtube.com/playlist?list=PL65E33789AA7052BC',
            'http://example.com/',
        ]
        for url in self.yt_links:
            result = utils.validate_video_url(url)
            self.assertEqual(
                result,
                'youtube',
                msg=('Invalid result "{0}" for url "{1}".'.format(
                    result, url)),
            )
        for url in self.vm_links:
            result = utils.validate_video_url(url)
            self.assertEqual(
                result,
                'vimeo',
                msg=('Invalid result "{0}" for url "{1}".'.format(
                    result, url)),
            )
        for url in self.invalid_links:
            result = utils.validate_video_url(url)
            self.assertIsNone(
                result,
                'Result should be "None" and not "{0}" for "{1}"'.format(
                    result, url
                )
            )
