from django.shortcuts import render,redirect
from .models import Post
from comments.models import Comment

# Create your views here.
def home_view(request,*arg,**kwargs):
	return render(request,'home.html',{})

def posts_view(request,*arg,**kwargs):
	posts = Post.objects.all()
	return render(request,'posts.html',{'posts':posts})

def single_post_view(request,id):
	try:
		post = Post.objects.get(id=id)
		comments = Comment.objects.filter(post=id)
		print(comments)
	except Post.DoesNotExist:
		return redirect("/")

	context = {
		'post':post,
		'comments':comments
	}
	return render(request,'posts_detail.html',context)