from django import forms
from django.contrib.auth.models import User

from .models import Post, Comment


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title",
                  "text",
                  "is_published",
                  "pub_date",
                  "location",
                  "category",
                  "image")

        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
                format='%Y-%m-%dT%H:%M',
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
