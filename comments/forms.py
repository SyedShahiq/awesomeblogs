from django import forms
from .models import Comment
#Django Model Form
class commentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = [
			'content',
		]