from django.db import models

from .querysets import PostQuerySet


class PublishedNowPostManager(models.Manager):
    def get_queryset(self):
        return (
            PostQuerySet(self.model)
            .join_related_data()
            .published_actualized()
        )
