"""Utilities for the ``media_library`` app."""
import re
VIMEO_PATTERN = re.compile('(?:https?://)?(?:www.)?(vimeo)(?:pro)?.com/(?:.*/)?(\d+)')  # NOQA
YOUTUBE_PATTERN = re.compile(
    '(?:https?://)?(?:(?:www\.)?(youtube)(?:\.\w{2,3})+/watch\?.*v=([a-zA-Z0-9_-]+)&?.*|(youtu\.be)/([a-zA-Z0-9_-]+))'  # NOQA
)
VIDEO_PATTERNS = [VIMEO_PATTERN, YOUTUBE_PATTERN]


def get_video_id(url):
    """Returns the video ID from a vimeo or YouTube URL."""
    video_id = ''
    if not url:
        return ''
    if validate_video_url(url) == 'vimeo':
        video_id = VIMEO_PATTERN.findall(url)[0][1]
    elif validate_video_url(url) == 'youtube':
        video_id = YOUTUBE_PATTERN.findall(url)[0][1]
    return video_id


def validate_video_url(url):
    """Validates, where the video was from."""
    for pattern in VIDEO_PATTERNS:
        result = pattern.search(url)
        if result is not None:
            # cast to list and remove NoneType values
            result = [res for res in result.groups() if res is not None]
            if len(result) == 2 and result[1] is not None:
                origin = result[0]
                if origin.startswith('youtu'):
                    return 'youtube'
                else:
                    return origin
    return
