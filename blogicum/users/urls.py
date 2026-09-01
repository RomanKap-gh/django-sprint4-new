from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        '<slug:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        '<slug:username>/edit/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
]
