from django.db import models
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def join_related_data(self):
        return self.select_related('author', 'category', 'location')

    def published_actualized(self):
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).filter(
            Q(category__is_published=True) | Q(category__isnull=True)
        ).order_by('-pub_date')

    def count_comments(self):
        return self.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
