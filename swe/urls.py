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

    path('forget-password', views.forget_password, name='forget_password'),

    path('forget-password/varification/', views.forget_password_varification, 
        name ='forget_password_varification'),

    # make sure that this path is always in last position
    # example.com/2016831035/
    path('<user_id>/', views.profile, name='profile')
]