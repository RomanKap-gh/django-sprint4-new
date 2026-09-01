from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    DetailView,
    UpdateView,
)

from .forms import ProfileForm
from blog.views import OnlyAuthorMixin

PROFILE_POSTS_LIMIT = 10


class ProfileDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user != self.object:
            queryset = self.object.posts.published_actualized()
        else:
            queryset = self.object.posts.all()
        paginator = Paginator(queryset, PROFILE_POSTS_LIMIT)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)


class ProfileUpdateView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    UpdateView
):
    model = User
    form_class = ProfileForm
    template_name = 'users/user.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse(
            'users:profile',
            kwargs={'username': self.object.username}
        )
