from django.shortcuts import render,redirect
from .models import Post
from comments.models import Comment
from comments.forms import commentForm
from django.http import JsonResponse
from django.core import serializers
import json
# Create your views here.
def home_view(request,*arg,**kwargs):
	return render(request,'home.html',{})

def posts_view(request,*arg,**kwargs):
	posts = Post.objects.all()
	return render(request,'posts.html',{'posts':posts})

def single_post_view(request,id):
	try:
		post = Post.objects.get(id=id)
		comments = Comment.objects.filter(post=id).order_by('-id')
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
		'comments_form':form
	}
	return render(request,'posts_detail.html',context)

def fetchAllPosts(request):
	posts = Post.objects.all()
	tmpJson = serializers.serialize("json",posts)
	tmpObj = json.loads(tmpJson)
	return JsonResponse({'posts':tmpJson})