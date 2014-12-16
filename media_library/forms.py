"""Forms for the ``media_library`` app."""
from django.utils.translation import get_language, ugettext_lazy as _

from hvad.forms import TranslatableModelForm
from multilingual_tags.forms.mixins import TaggingFormMixin

from . import models


class MediaItemImageForm(TaggingFormMixin, TranslatableModelForm):
    """Form to edit and create meta data for library images."""

    language = get_language()
    tag_field = {
        'name': 'tags',
        'label': _('Tags'),
        'help_text': _('You can add up to 3 tags separated by comma.'),
        'required': False,
        'max_tags': 3,
    }

    def __init__(self, user, image, *args, **kwargs):
        super(MediaItemImageForm, self).__init__(*args, **kwargs)
        self.image = image
        try:
            self.library = user.medialibraries.all()[0]
        except IndexError:
            self.library = models.MediaLibrary.objects.create(user=user)
        self.fields['date'].widget.attrs.update({'data-class': 'datepicker'})

    def save(self, commit=True):
        self.instance.library = self.library
        self.instance.image = self.image
        return super(MediaItemImageForm, self).save(commit)

    class Meta:
        model = models.MediaItem
        fields = ['date', 'location']


class MediaItemVideoForm(TaggingFormMixin, TranslatableModelForm):

    language = get_language()
    tag_field = {
        'name': 'tags',
        'label': _('Tags'),
        'help_text': _('You can add up to 3 tags separated by comma.'),
        'required': False,
        'max_tags': 3,
    }

    def __init__(self, user, *args, **kwargs):
        super(MediaItemVideoForm, self).__init__(*args, **kwargs)
        try:
            self.library = user.medialibraries.all()[0]
        except IndexError:
            self.library = models.MediaLibrary.objects.create(user=user)
        self.fields['date'].widget.attrs.update({'data-class': 'datepicker'})

    def save(self, commit=True):
        self.instance.library = self.library
        return super(MediaItemVideoForm, self).save(commit)

    class Meta:
        model = models.MediaItem
        fields = ['video', 'date', 'location']
