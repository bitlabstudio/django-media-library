"""URLs for the ``media_library`` app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^edit/$', views.MediaLibraryEditView.as_view(),
        name='medialibrary_edit'),
    url(r'^upload/$', views.MediaLibraryUploadView.as_view(),
        name='medialibrary_upload'),
    url(r'^image/create/(?P<image_pk>\d+)/$',
        views.MediaItemImageCreateView.as_view(),
        name='mediaitem_image_create'),
    url(r'^image/update/(?P<image_pk>\d+)/$',
        views.MediaItemImageUpdateView.as_view(),
        name='mediaitem_image_update'),
    url(r'^video/create/$',
        views.MediaItemVideoCreateView.as_view(),
        name='mediaitem_video_create'),
    url(r'^video/update/(?P<pk>\d+)/$',
        views.MediaItemVideoUpdateView.as_view(),
        name='mediaitem_video_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        views.MediaItemDeleteView.as_view(),
        name='mediaitem_delete'),
)
