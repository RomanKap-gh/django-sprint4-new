from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment

POST_BY_PAGE = 10


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post.objects, pk=post_id)
        if self.request.user != post.author:
            if (
                post.pub_date > timezone.now()
                or not post.is_published
                or not post.category.is_published
            ):
                raise Http404("Публикация не найдена или недоступна")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.all()
        )
        return context


class CategoryPostsListView(ListView):
    model = Category
    ordering = 'id'
    paginate_by = POST_BY_PAGE
    template_name = 'blog/category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=kwargs['category_slug'],
            is_published=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.category.posts(manager='published_now').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'users:profile',
            kwargs={'username': self.object.author.username}
        )


class PostListView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = POST_BY_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published_now.all()


class PostUpdateView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    UpdateView,
):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_authenticated or request.user != obj.author:
            return redirect('blog:post_detail', post_id=obj.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class PostDeleteView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    DeleteView,
):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'users:profile',
            kwargs={'username': self.object.author.username}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_obj = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def form_invalid(self, form):
        context = {
            'post': self.post_obj,
            'comments': self.post_obj.comments.all().order_by('created_at'),
            'form': form,
        }
        return render(self.request, 'blog/detail.html', context)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.post_obj.pk}
        )


class CommentUpdateView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    UpdateView
):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class CommentDeleteView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    DeleteView
):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )
