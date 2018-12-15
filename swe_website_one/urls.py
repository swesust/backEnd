from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path("bulma/", views.bulma, name='bulma'),
    path('registration/', views.registration, name='registration'),
    path('accounts/', include('django.contrib.auth.urls')),
]
