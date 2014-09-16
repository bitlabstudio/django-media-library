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
