from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path("bulma/", views.bulma, name='bulma'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('batch/', views.batchlist, name='batchlist'),

    # a particular batch list: example.com/batch/2017
    path('batch/<batch_id>/', views.batch, name='batch'),

    path('accounts/', include('django.contrib.auth.urls')),
]
