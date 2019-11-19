from django.shortcuts import render,redirect
from .models import Post
from django.contrib.auth.models import User
from comments.models import Comment,Reply
from comments.forms import commentForm
from django.http import JsonResponse
from django.core import serializers
import json
# Create your views here.
def home_view(request,*arg,**kwargs):
	return render(request,'home.html',{})

def posts_view(request,*arg,**kwargs):
	posts = Post.objects.all()
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