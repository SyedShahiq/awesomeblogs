from django.shortcuts import render,redirect
from .models import Post
from comments.models import Comment
from comments.forms import commentForm

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
		form = commentForm(request.POST or None)
		if request.method == 'POST':
			comment = request.POST.get('content')
			Comment.objects.create(content=comment, post=post)
			return redirect("/post/"+str(id))
	except Post.DoesNotExist:
		return redirect("/")

	context = {
		'post':post,
		'comments':comments,
		'comments_form':form
	}
	return render(request,'posts_detail.html',context)