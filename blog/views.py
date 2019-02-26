from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post, Comment
from .forms import PostForm, CommentForm

import markdown


def about(request):
    """
    homepage
    :param request:
    :return:
    """
    return render(request, 'main/about.html')


def research(request):
    """
    Page where I detail the submitted papers
    :param request:
    :return:
    """
    return render(request, 'main/research.html')


def post_list(request):

    """
    List of posts on homepage
    :param request:
    :return:
    """

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    for i in range(len(posts)):
        posts[i].text = markdown.markdown(posts[i].text)
    return render(request, 'main/blog.html', {'posts': posts})


@login_required
def post_draft_list(request):

    """
     List of unpublished posts (drafts)
    :param request:
    :return:
    """

    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_detail(request, post_id):
    """
    :param request:
    :param post_id:
    :return:
    """

    if request.method == "POST":
        add_comment(request, post_id)

    form = CommentForm()
    post = get_object_or_404(Post, pk=post_id)
    post.text = markdown.markdown(post.text, extensions=['markdown.extensions.codehilite'])
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


@login_required
def post_new(request):
    """
    Form to add a new post
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """
    Form to edit a post
    :param request:
    :param post_id:
    :return:
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_publish(request, post_id):
    """
    Publish a post
    :param request:
    :param post_id:
    :return:
    """
    post = get_object_or_404(Post, pk=post_id)
    post.publish()
    return redirect('post_detail', post_id=post_id)


@login_required
def post_remove(request, post_id):
    """
    Remove a post
    :param request:
    :param post_id:
    :return:
    """
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('post_list')


def add_comment(request, post_id):
    """
    Form to add a comment to a post
    :param request:
    :param post_id:
    :return:
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        print(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        return redirect('post_detail', post_id=post.pk)


@login_required
def remove_comment(request, comment_id):
    """
    Remove a comment
    :param request:
    :param comment_id:
    :return:
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('post_detail', post_id=comment.post.pk)


@login_required
def approve_comment(request, comment_id):
    """
    approve a comment
    :param request:
    :param comment_id:
    :return:
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.approve()
    return redirect('post_detail', post_id=comment.post.pk)
