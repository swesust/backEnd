from . import views
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path("bulma/", views.bulma, name='bulma'),
    path('login/', views.login, name='login'),
    path('batch/', views.batchlist, name='batchlist'),
   	path('faculty/', views.faculty, name='faculty'),

    # a particular batch list: example.com/batch/2017
    path('batch/<batch_id>/', views.batch, name='batch'),
    path('test/', views.test, name='test'),
    path('<user_id>/', views.profile, name='profile'),

    path('accounts/', include('django.contrib.auth.urls')),
]

#eaxa.com/login/