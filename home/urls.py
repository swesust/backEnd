from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path("bulma/", views.bulma, name='bulma'),
    path('login/', views.login, name='login'),
    path('batch/', views.batchlist, name='batchlist'),
   	path('faculty/', views.faculty, name='faculty'),

    # a particular batch list: example.com/batch/2017
    path('batch/<batch_id>/', views.batch, name='batch'),

    path('accounts/', include('django.contrib.auth.urls')),
]
