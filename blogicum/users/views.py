from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

import core.constants as constants

from .forms import ProfileForm

User = get_user_model()


class ProfileDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.object.posts.count_comments()
        if self.request.user != self.object:
            queryset = queryset.join_related_data().published_actualized()
        else:
            queryset = queryset.filter(category__isnull=False)
        paginator = Paginator(queryset, constants.POST_BY_PAGE)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)


class ProfileUpdateView(
    LoginRequiredMixin,
    UpdateView
):
    model = User
    form_class = ProfileForm
    template_name = 'users/user.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'users:profile',
            kwargs={'username': self.object.username}
        )
