from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category


def check_post_published(post: Post):
    if ((not post.is_published)
            or (post.pub_date > timezone.now())
            or (not post.category.is_published)):
        raise Http404


def index(request):
    posts = (Post.objects.filter(is_published=True,
                                 pub_date__lte=timezone.now(),
                                 category__is_published=True)[:5]
             .select_related('category')
             .select_related('author')
             .select_related('location'))
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    check_post_published(post)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404
    posts = (category.posts.filter(is_published=True,
                                   pub_date__lte=timezone.now())
             .select_related('category')
             .select_related('location')
             .select_related('author'))
    return render(request, 'blog/category.html',
                  {'category': category_slug,
                   'post_list': posts})
