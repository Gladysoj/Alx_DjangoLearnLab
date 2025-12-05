# blog/forms.py
from taggit.forms import TagWidget
from django import forms
from .models import Post, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

class PostForm(forms.ModelForm):
    # Comma-separated tags input; we’ll parse in the view
    tags_input = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g., django, web, backend)"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags_input']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a descriptive title'}),
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Write your post...'}),
            'tags': TagWidget(),
        }

    def clean_tags_input(self):
        raw = self.cleaned_data.get('tags_input', '')
        # Normalize: split, strip, deduplicate, ignore empties
        names = [t.strip() for t in raw.split(',') if t.strip()]
        # Optional simple validation: limit length and count
        if any(len(n) > 50 for n in names):
            raise forms.ValidationError("Tag names must be 50 characters or fewer.")
        if len(names) > 20:
            raise forms.ValidationError("Too many tags; limit to 20.")
        return list(dict.fromkeys(names))  # unique order-preserving

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment...'}),
        }

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if len(content) < 2:
            raise forms.ValidationError('Comment is too short.')
        return content