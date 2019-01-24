from . import views
from django.urls import path, include

from django.contrib.auth import views as resetviews
urlpatterns = [
    # example.com/
    path('', views.index, name='index'),
    # example.com/login/
    path('login/', views.login, name='login'),
    # example.com/logout/
    path('logout/', views.logout, name='logout'),
    # example.com/batch/
    path('batch/', views.batchlist, name='batchlist'),
    # example.com/faculty/
   	path('faculty/', views.faculty, name='faculty'),
    # example.com/feeds/
   	path('feeds/', views.feeds, name='feeds'),
    # example.com/batch/2016/
    path('batch/<batch_id>/', views.batch, name='batch'),
    # example.com/forget-password/
    path('forget-password/', views.forget_password, name='forget_password'),
    # example.com/forget-password/varification/
    path('forget-password/varification/', views.forget_password_varification, 
        name ='forget_password_varification'),
    # example.com/feeds/delete/10/
    path('feeds/delete/<pk>/', views.feed_delete, name='feed_delete' ),
    
    # example.com/2016831035/edit/
    path('<user_id>/edit', views.profile_edit, name='profile_edit'),
    # make sure that this path is always in last position to avoid conflict
    # example.com/2016831035/
    path('<user_id>/', views.profile, name='profile')
]