import json

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from blog.models import Post

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

def fetch_user_detail(request,id):
	user = User.objects.get(id=id)
	response = JsonResponse({'username':user.username,'email':user.email})
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
	return response

def fetch_all_users(request):
    users = User.objects.all()
    tmpJson = serializers.serialize("json",users)
    tmpObj = json.loads(tmpJson)
    response = JsonResponse({'users':tmpJson})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response