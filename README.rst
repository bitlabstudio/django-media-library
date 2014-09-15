Django Media Library
====================

A reusable Django app to let users organize their own media.

If you intend to manage files like images, pdfs or simliar as an admin, you might be interested in django-document-library_.
.. _django-document-library: https://github.com/bitmazk/django-document-library


Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-media-library

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/mbrochh/django-reusable-app-template.git#egg=media_library

TODO: Describe further installation steps (edit / remove the examples below):

Add ``media_library`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'media_library',
    )

Add the ``media_library`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^media-library/', include('media_library.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load media_library_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate media_library


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
