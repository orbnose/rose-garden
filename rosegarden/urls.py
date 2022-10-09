from django.urls import path
from . import views

app_name = 'rosegarden'
urlpatterns = [
    path('', views.homepage, name='index'),
    path('books/', views.homepage),
    path('books/<int:book_pk>/', views.bookDetails, name='book_details'),
    path('books/<int:book_pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_pk>/delete/', views.delete_book, name='delete_book'),
    path('search/', views.search, name='search'),
    path('branches/', views.branchList, name='branch_list'),
    path('branches/<int:branch_pk>', views.branchDetails, name='branch_details'),
    path('users/', views.userList, name='user_list'),
    path('users/<str:username>',views.userDetails, name='user_details'),
    path('users/<str:username>/edit/',views.userEdit, name='edit_user'),
    path('add_book/', views.add_book, name='add_book'),
    path('how_to/', views.how_to, name="how_to")
]