from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login

from .forms import UserRegisterForm
# Create your views here.
def user_registration(request):
	if request.user.is_authenticated:
		return redirect("posts")
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Welcome to Awesome Blogs')
			user = authenticate(username = form.cleaned_data['username'],password=form.cleaned_data['password1'])
			login(request,user)
			return redirect("posts")
	else:
		form = UserRegisterForm()
	return render(request,'register.html',{'form':form})
