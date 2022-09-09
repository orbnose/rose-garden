from django.urls import path
from . import views

app_name = 'rosegarden'
urlpatterns = [
    path('', views.homepage, name='index')
]