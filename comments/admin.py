from django.contrib import admin

# Register your models here.
from .models import Comment
from .models import Reply

admin.site.register(Comment)
admin.site.register(Reply)
