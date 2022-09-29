# Rose Garden

Rose Garden is a Django app for displaying the books in my personal library.


Quick start
-----------
1. Run python -m pip install git+https://github.com/orbnose/rose-garden#egg=rose-garden

2. Add "rosegarden" to your INSTALLED_APPS setting like this:

```
    INSTALLED_APPS = [
        ...
        'rosegarden.apps.RosegardenConfig',
    ]
```

3. Include the polls URLconf in your project urls.py like this:

```
urlpatterns = [
    ...
    path('rosegarden/', include('rosegarden.urls')),
]
```

4. Run ``python manage.py migrate`` to create the Rose Garden models.
