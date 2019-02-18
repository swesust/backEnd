from django.contrib.auth import views as resetviews
from django.urls import path, include
from .views import *

urlpatterns = [
    # example.com/
    path('', view.index, name='index'),
    # example.com/login/
    path('login/', auth.login, name='login'),
    # example.com/logout/
    path('logout/', auth.logout, name='logout'),
    # example.com/batch/
    path('batch/', view.batchlist, name='batchlist'),
    # example.com/faculty/
   	path('faculty/', view.faculty, name='faculty'),
    # example.com/feeds/
   	path('feeds/', feed.all, name='feeds'),
    # example.com/batch/2016/
    path('batch/<batch_id>/', view.batch, name='batch'),
    # example.com/forget-password/
    path('forget-password/', auth.forget_password, name='forget_password'),
    # example.com/forget-password/varification/
    path('forget-password/varification/', auth.forget_password_varification, 
        name ='forget_password_varification'),
    path('change-password/', auth.change_password, name='change_password'),
    # example.com/feeds/post/create
    path('feeds/post/create/', feed.create, name='post_create'),
    # example.com/feeds/post/edit/10/
    path('feeds/post/edit/<pk>/', feed.edit, name='edit_post'),
    # example.com/feeds/post/delete/10/
    path('feeds/post/delete/<pk>/', feed.delete, name='post_delete' ),
    # a full post
    path('feeds/post/<pk>/', feed.single ,name='single_post'),
    # example.com/2016831035/edit/
    path('<user_id>/edit/', user.edit, name='profile_edit'),
    # example.com/2016831035/endrosement/add/
    path('<user_id>/endrosement/add/', endrosement.add, name='endrosement_add'), 
    # example.com/2016831035/endrosement/delete/10/
    path('<user_id>/endrosement/delete/<pk>/', endrosement.delete, name='endrosement_delete'),
    # example.com/2016831035/endrosement/edit/10/
    path('<user_id>/endrosement/edit/<pk>/', endrosement.edit, name='endrosement_edit'),
    # example.com/2016831035/working/add
    path('<user_id>/working/add/', working.add, name='working_add'),
    # example.com/2016831035/working/edit/10/
    path('<user_id>/working/edit/<pk>/', working.edit, name='working_edit'),
    # example.com/2016831035/working/delete/10
    path('<user_id>/working/delete/<pk>/', working.delete, name='working_delete'),
    # search
    path('search/', view.search, name='search'),
    # make sure that this path is always in last position to avoid conflict
    # example.com/2016831035/
    path('<user_id>/', user.profile, name='profile')
]