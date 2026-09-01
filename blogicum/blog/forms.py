from django import forms
from django.core.exceptions import ValidationError

from core.constants import MODERATION_ERROR

from .models import Post, Comment
from .moderation import is_toxic


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'pub_date',
            'location',
            'category',
            'image',
        )
        widgets = {
            'birthday': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'},
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        comment = self.cleaned_data['text']
        if is_toxic(comment):
            raise ValidationError(MODERATION_ERROR)

        return comment
