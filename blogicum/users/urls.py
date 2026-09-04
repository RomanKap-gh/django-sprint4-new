from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'edit/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        '<str:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
]
