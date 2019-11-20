import json

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Count

from comments.models import Comment,Reply
from comments.forms import commentForm
from .models import Post,emotions

# Create your views here.
def home_view(request,*arg,**kwargs):
	return render(request,'home.html',{})

def posts_view(request,*arg,**kwargs):
	posts = Post.objects.raw('SELECT blog_post.id , blog_post.title ,blog_post.content,blog_post.date_posted,blog_post.author_id, COUNT(blog_emotions.post_id) as count FROM blog_post LEFT JOIN blog_emotions ON blog_post.id = blog_emotions.post_id GROUP BY blog_post.id ORDER BY blog_post.id DESC')
	users = User.objects.all()
	return render(request,'posts.html',{'posts':posts,'users':users})

def posts_by_user(request,id):
	user_posts = Post.objects.filter(author=id)
	return render(request,'user_posts.html',{'posts':user_posts})

def single_post_view(request,id):
	try:
		last_post = Post.objects.last()
		post = Post.objects.get(id=id)
		comments = Comment.objects.filter(post=id).order_by('-id')
		comment_ids_list = []
		for comment in comments:
			comment_ids_list.append(comment.id)
		replies = Reply.objects.filter(comment__in = comment_ids_list)
		form = commentForm(request.POST or None)
		if request.method == 'POST' and form.is_valid():
			comment = request.POST.get('content')
			Comment.objects.create(content=comment, post=post, user=request.user)
			return redirect("/post/"+str(id))
	except Post.DoesNotExist:
		return redirect("/")

	context = {
		'post':post,
		'comments':comments,
		'comments_form':form,
		'replies':replies,
		'last_post':last_post
	}
	return render(request,'posts_detail.html',context)

def fetchAllPosts(request):
	posts = Post.objects.all()
	tmpJson = serializers.serialize("json",posts)
	tmpObj = json.loads(tmpJson)
	response = JsonResponse({'posts':tmpJson})
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
	return response

def add_emotion(request,id):
	if request.method == 'POST':
		post = Post.objects.get(id=id)
		check_present_emotion = emotions.objects.filter(user=request.user).filter(post=post)
		if check_present_emotion.count() == 0:
			emotions.objects.create(like=1,post=post,user=request.user)
		else:
			return JsonResponse({'like':'false'})
	return JsonResponse({'like':'true'})