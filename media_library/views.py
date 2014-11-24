"""Views for the ``media_library`` app."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)
from django.shortcuts import get_object_or_404

from django_libs.views_mixins import AjaxResponseMixin
from multilingual_tags.models import Tag
from user_media.models import UserMediaImage

from . import models
from . import forms


# Mixins ======================================================================

class MediaItemImageCRUDViewMixin(object):
    form_class = forms.MediaItemImageForm
    model = models.MediaItem
    template_name = 'media_library/mediaitem_image_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.image = get_object_or_404(
            UserMediaImage, pk=kwargs.get('image_pk'),
        )
        if self.image.user != request.user:
            raise Http404
        return super(MediaItemImageCRUDViewMixin, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(MediaItemImageCRUDViewMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user, 'image': self.image})
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(MediaItemImageCRUDViewMixin, self).get_context_data(
            **kwargs)
        tags = [str(t.name) for t in Tag.objects.get_for_model(self.model)]
        ctx.update({'image': self.image, 'tags': tags})
        return ctx

    def get_success_url(self):
        if 'success_url' in self.request.REQUEST:
            return self.request.REQUEST.get('success_url')
        return reverse('medialibrary_edit')


class MediaItemVideoCRUDViewMixin(CreateView):
    form_class = forms.MediaItemVideoForm
    model = models.MediaItem
    template_name = 'media_library/mediaitem_video_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            self.object = self.get_object(self.queryset)
            if self.object.library.user != request.user:
                raise Http404
        return super(MediaItemVideoCRUDViewMixin, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MediaItemVideoCRUDViewMixin, self).get_context_data(
            **kwargs)
        tags = [str(t.name) for t in Tag.objects.get_for_model(self.model)]
        ctx.update({'tags': tags})
        return ctx

    def get_form_kwargs(self):
        kwargs = super(MediaItemVideoCRUDViewMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        if 'success_url' in self.request.REQUEST:
            return self.request.REQUEST.get('success_url')
        return reverse('medialibrary_edit')


# Views =======================================================================

class MediaLibraryEditView(AjaxResponseMixin, DetailView):
    """A view to edit media details of a user on its profile."""
    template_name = 'media_library/medialibrary_edit.html'
    model = models.MediaLibrary

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MediaLibraryEditView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MediaLibraryEditView, self).get_context_data(**kwargs)
        new_images = self.object.user_media_images.filter(
            media_items__isnull=True,
        )
        ctx.update({'new_images': new_images})
        return ctx

    def get_object(self, queryset=None):
        library, created = models.MediaLibrary.objects.get_or_create(
            user=self.request.user
        )
        return library


class MediaItemDeleteView(DeleteView):
    model = models.MediaItem
    template_name = 'media_library/mediaitem_delete.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        if self.object.library.user != request.user:
            raise Http404
        return super(MediaItemDeleteView, self).dispatch(
            request, *args, **kwargs)

    def get_success_url(self):
        if 'success_url' in self.request.REQUEST:
            return self.request.REQUEST.get('success_url')
        return reverse('medialibrary_edit')


class MediaItemImageCreateView(MediaItemImageCRUDViewMixin, CreateView):
    """View to create meta data for a media item."""


class MediaItemImageUpdateView(MediaItemImageCRUDViewMixin, UpdateView):
    """View to update meta data for a media item."""

    def get_object(self, queryset=None):
        return self.image.media_items.all()[0]


class MediaItemVideoCreateView(MediaItemVideoCRUDViewMixin, CreateView):
    """View to create meta data for a media item."""


class MediaItemVideoUpdateView(MediaItemVideoCRUDViewMixin, UpdateView):
    """View to update meta data for a media item."""


class MediaLibraryUploadView(TemplateView):
    """View where users upload their pictures."""
    template_name = "media_library/medialibrary_upload.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MediaLibraryUploadView, self).dispatch(request, *args,
                                                            **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MediaLibraryUploadView, self).get_context_data(**kwargs)
        ctx.update({'library': self.request.user.medialibraries.all()[0]})
        return ctx
