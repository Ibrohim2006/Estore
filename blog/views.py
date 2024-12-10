from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import PostModel, TagModel, CommentModel
from .forms import NewsletterForm, CommentForm
from django.db.models import Count, Q


def blog_view(request):
    page_number = request.GET.get('page')
    search_query = request.GET.get('search', '')
    if search_query:
        posts = PostModel.objects.filter(
            Q(title__icontains=search_query) | Q(tag__name__icontains=search_query)
        ).annotate(comment_count=Count('commentmodel'))
    else:
        posts = PostModel.objects.annotate(comment_count=Count('commentmodel'))
    tags = TagModel.objects.annotate(post_count=Count('postmodel'))
    most_commented_posts = PostModel.objects.annotate(comment_count=Count('commentmodel')) \
                               .order_by('-comment_count')[:6]
    paginator = Paginator(posts, 4)
    page_obj = paginator.get_page(page_number)

    form = NewsletterForm()
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:blog')

    context = {
        'posts': page_obj,
        'form': form,
        'tags': tags,
        'most_commented_posts': most_commented_posts,
    }
    return render(request, 'blog/blog.html', context)


def blog_detail_view(request, slug):
    post = PostModel.objects.annotate(comment_count=Count('commentmodel')).get(slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog:blog_detail', slug=post.slug)
    else:
        form = CommentForm()

    prev_post = PostModel.objects.filter(created_at__lt=post.created_at).order_by('-created_at').first()
    next_post = PostModel.objects.filter(created_at__gt=post.created_at).order_by('created_at').first()

    comments = CommentModel.objects.filter(post=post).order_by('-created_at')[:4]
    d = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/single-blog.html', context=d)


def tag_view(request, slug):
    tag = get_object_or_404(TagModel, slug=slug)
    posts = PostModel.objects.filter(tag=tag)

    d = {
        'posts': posts
    }
    return render(request, 'blog/tag.html', context=d)
