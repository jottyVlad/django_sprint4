from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import (UserChangeForm,
                    PostForm,
                    CommentForm,
                    UserChangePasswordForm)
from .models import Post, Category, Comment
from .paginator import paginate


def check_post_published(post: Post, user: User):
    if not (post.is_published
            and post.pub_date <= timezone.now()
            or post.author == user):
        raise Http404


def index(request):
    posts = (Post.objects.filter(is_published=True,
                                 pub_date__lte=timezone.now(),
                                 category__is_published=True)
             .select_related('category')
             .select_related('author')
             .select_related('location'))

    posts = posts.annotate(comment_count=Count('comments'))

    page_obj = paginate(posts, request)
    return render(request,
                  'blog/index.html',
                  {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    check_post_published(post, request.user)

    form = CommentForm()
    ctx = {
        'post': post,
        'form': form,
        'comments': post.comments.all(),
    }

    return render(request,
                  'blog/detail.html',
                  ctx)


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()

    return render(request,
                  "blog/create.html",
                  {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request,
                  "blog/create.html",
                  {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect("blog:post_detail", post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
        else:
            return

    form = CommentForm(instance=comment)
    return render(request, "blog/comment.html",
                  {"form": form, "comment": comment})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)

    form = PostForm(instance=post)

    return render(request,
                  "blog/create.html",
                  {"form": form, "post": post})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)

    return render(request,
                  "blog/comment.html",
                  {"comment": comment, "form": None})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404
    posts = (category.posts.filter(is_published=True,
                                   pub_date__lte=timezone.now())
             .select_related('category')
             .select_related('location')
             .select_related('author'))

    page_obj = paginate(posts, request)
    return render(request, 'blog/category.html',
                  {'category': category,
                   'page_obj': page_obj})


def get_profile_or_404(request, username):
    profile = get_object_or_404(get_user_model(),
                                username=username)

    if profile == request.user:
        posts = profile.posts.all() # noqa
    else:
        posts = profile.posts.filter(is_published=True,  # noqa
                                     pub_date__lte=timezone.now(),
                                     category__is_published=True)

    posts = posts.annotate(comment_count=Count("comments"))
    page = paginate(posts, request)

    ctx = {
        'profile': profile,
        'page_obj': page,
    }
    return render(
        request, "blog/profile.html", ctx
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("blog:profile", username=request.user.username)

    else:
        form = UserChangeForm(instance=request.user)

    return render(request, "blog/user.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = UserChangePasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("blog:profile", username=request.user.username)
        else:
            return render(request,
                          "registration/change_password_form.html",
                          {"form": form})
