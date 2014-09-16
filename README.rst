Django Media Library
====================

A reusable Django app to let users organize their own media.

Note! Django 1.7 support is WIP.

If you intend to manage files like images, pdfs or simliar as an admin, you might be interested in django-document-library_.

.. _django-document-library: https://github.com/bitmazk/django-document-library


It enables users to upload images and add Vimeo or YouTube video links into their own gallery.


Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-media-library

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-media-library.git#egg=media_library

TODO: Describe further installation steps (edit / remove the examples below):

Add ``media_library`` and its dependencies to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'media_library',
        'multilingual_tags',
        'generic_positions',
        'user_media',
        'hvad',
    )

Add the ``media_library``, ``user_media`` and ``generic_positions`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^pos/', include('generic_positions.urls')),
        url(r'^umedia/', include('user_media.urls')),
        url(r'^media-library/', include('media_library.urls')),
    )

If you stick to the default templates or want to derive your own from them, you
might also want to add the default styles and our simple image and video preview script.

.. code-block:: html

    {% load static %}

    <link href="{% static "media_libraray/media_library.css" %}" rel="stylesheet">
    <script src="{% static "media_library/preview.js" %}"></script>


Add the ``django-user-media`` scripts to your templates to have the file upload.

.. code-block:: html

    {% load static %}

    {# you will also need jquery and jquery-ui. #}
    <script src="{% static "js/jquery-1.11.1.js" %}"></script>
    <script src="{% static "js/jquery-ui-1.11.1.min.js" %}"></script>

    {% include "user_media/partials/image_upload_scripts.html" %}

You can read up more information and advanced usage at the django-user-media_ page.

.. _django-user-media: https://github.com/bitmazk/django-user-media

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate


Not necessary, but highly recommended
-------------------------------------


To have the drag and drop re-ordering enabled, you will need to add the ``reorder.js`` script to your templates.

E.g. add the following to your base template:

.. code-block:: html

    {% load static %}

    <script type="text/javascript" src="{{ STATIC_URL }}generic_positions/js/reorder.js"></script>


Also check django-generic-positions_ for further information on positioning.

.. _django-generic-positions: https://github.com/bitmazk/django-generic-positions


For the tagging plugin, please add the ``typeahead.tagging.js`` and ``typeahead.bundle.min.js``
as well as styles to your templates as well, which are part of ``django-multilingual-tags``.

.. code-block:: html

    {% load static %}

    {# Plain Bootstrap-like styles. #}
    <link href="{% static "multilingual_tags/css/typeahead.tagging.css" %}" rel="stylesheet" media="screen">

    {# And then there's typeahead and the tagging plugin. #}
    <script src="{% static "multilingual_tags/js/typeahead.bundle.min.js" %}"></script>
    <script src="{% static "multilingual_tags/js/typeahead.tagging.js" %}"></script>


For more info on the tagging app, check out django-multilingual-tags_.

.. _django-multilingual-tags: https://github.com/bitmazk/django-multilingual-tags


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-media-library
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
