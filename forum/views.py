from django.shortcuts import render
from forum.models import Post, Comment
from forum.forms import CommentForm, PostForm

# Create your views here.
def home_view(request):
    posts = Post.objects.all().order_by('-created_on')
    
    context = {
        "posts": posts,
    }
    return render(request, 'home.html', context)

def forum_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
    }
    return render(request, "forum_index.html", context)

def forum_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "forum_category.html", context)

def forum_detail(request, pk):
    post = Post.objects.get(pk=pk)
    project_file = post.project_file

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "form" : form,
        "comments": comments,
        'project_file': project_file
    }

    return render(request, "forum_detail.html", context)