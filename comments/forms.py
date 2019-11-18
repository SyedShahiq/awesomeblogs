from django import forms
from .models import Comment
#Django Model Form
class commentForm(forms.ModelForm):
	content = forms.CharField(label='Comment',widget=forms.Textarea({
		'placeholder':'Please share your valueable comments',
		'class': 'form-group'
		}))
	class Meta:
		model = Comment
		fields = [
			'content',
		]