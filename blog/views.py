import base64
import json
import pickle
from ast import literal_eval

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render

import redis
from comments.forms import commentForm
from comments.models import Comment, Reply
from phpserialize import *

from .forms import PostEditForm
from .models import Post, emotions


def home_view(request, *arg, **kwargs):
    # r = redis.Redis(host='127.0.0.1', port=6379, db=0,decode_responses=True)
    # keys = r.keys("PHPREDIS_SESSION:*")
    # user_key = str(keys[0])
    # print(user_key)
    # user_bytes = r.get(user_key)
    # user_obj = loads(user_bytes.encode('utf-8'))
    # user = user_obj[b'user'].decode('utf-8')
    # user_details = json.loads(user)
    # try_login = authenticate(username=user_details['username'],password=user_details['password'])
    # login(request,try_login)
    request.session['username'] = 'Shahiq'
    request.session['test'] = 'Test'
    request.session['another'] = 'Yet Another'
    return render(request, 'home.html', {})


def posts_view(request, *arg, **kwargs):
    posts = Post.objects.raw('SELECT blog_post.id , blog_post.title ,blog_post.content,blog_post.date_posted,blog_post.author_id, COUNT(blog_emotions.post_id) as count FROM blog_post LEFT JOIN blog_emotions ON blog_post.id = blog_emotions.post_id GROUP BY blog_post.id ORDER BY blog_post.id DESC')
    users = User.objects.all()
    return render(request, 'posts.html', {'posts': posts, 'users': users})


def posts_by_user(request, id):
    user_posts = Post.objects.filter(author=id).order_by('-id')
    return render(request, 'user_posts.html', {'posts': user_posts})


def single_post_view(request, id):
    try:
        last_post = Post.objects.last()
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post=id).order_by('-id')
        comment_ids_list = []
        for comment in comments:
            comment_ids_list.append(comment.id)
        replies = Reply.objects.filter(comment__in=comment_ids_list)
        form = commentForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            comment = request.POST.get('content')
            Comment.objects.create(content=comment, post=post, user=request.user)
            return redirect("/post/"+str(id))
    except Post.DoesNotExist:
        return redirect("/")

    context = {
        'post': post,
        'comments': comments,
        'comments_form': form,
        'replies': replies,
        'last_post': last_post
    }
    return render(request, 'posts_detail.html', context)


def fetchAllPosts(request):
    posts = Post.objects.all()
    tmpJson = serializers.serialize("json", posts)
    tmpObj = json.loads(tmpJson)
    response = JsonResponse({'posts': tmpJson})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response


def posts_by_user_api(request, id):
    user_posts = Post.objects.filter(author=id).order_by('-id')
    tmpJson = serializers.serialize("json", user_posts)
    tmpObj = json.loads(tmpJson)
    response = JsonResponse({'posts': tmpJson})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response


def add_emotion(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        check_present_emotion = emotions.objects.filter(user=request.user).filter(post=post)
        if check_present_emotion.count() == 0:
            emotions.objects.create(like=1, post=post, user=request.user)
        else:
            return JsonResponse({'like': 'false'})
    return JsonResponse({'like': 'true'})


@login_required
def edit_posts(request, id):
    post = Post.objects.get(id=id)
    title = post.title
    form = PostEditForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("posts")
    return render(request, 'posts_edit.html', {'form': form, 'post_title': title})


def create_posts(request):
    form = PostEditForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect("posts")
    return render(request, 'posts_creation.html', {'form': form})


def delete_post(request, id):
    query = Post.objects.get(id=id)
    if query.author == request.user:
        query.delete()
        messages.success(request, 'Post Deleted Successfully')
        return redirect("/post/user/"+str(request.user.id))
    else:
        messages.error(request, 'Unable to delete this post')
        return redirect("home")
