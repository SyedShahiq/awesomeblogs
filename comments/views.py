from django.shortcuts import render
from .models import Reply,Comment
from django.http import JsonResponse
import json
# Create your views here.
def createNewReply(request):
	print(request.body)
	data = json.loads(request.body)
	print(data['comment_id'])
	if request.method == 'POST':
		comment = Comment.objects.get(id = int(data['comment_id']))
		Reply.objects.create(content=data['content'],comment=comment,user=request.user)
	return JsonResponse({'posts':'dasdas'})
