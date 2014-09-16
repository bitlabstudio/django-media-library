"""Utilities for the ``media_library`` app."""
import re

from django.http.request import QueryDict


def get_video_id(url):
    """Returns the video ID from a vimeo or YouTube URL."""
    video_id = ''
    vimeo_pattern = re.compile('vimeo.com.*/(\d+)')
    if not url:
        return ''
    if 'youtube' in url:
        query = url.split('?')[-1]
        querydict = QueryDict(query, mutable=True)
        video_id = querydict.get('v')
    else:
        video_id = vimeo_pattern.findall(url)[0]
    return video_id
