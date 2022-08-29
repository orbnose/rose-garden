# rose-garden
Django app for displaying the books in my personal library

=====
Rose Garden
=====

Rose Garden is a Django app for displaying the books in my personal library.


Quick start
-----------
1. Run python -m pip install git+https://github.com/orbnose/rose-garden#egg=rose-garden

1. Add "rosegarden" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rosegarden',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('rosegarden/', include('rosegarden.urls')),

3. Run ``python manage.py migrate`` to create the Rose Garden models.
