from django import forms
from .models import Comment
"""
1. Django comes with two base form class
    Form: To build standard forms for rendering on our templates
    ModelForm: Used to build forms to create and update model instances
2. Here we use forms.Form class(EmailPostForm) to get the name, email, to and comments for the post to be shared
3. We use a textarea widget for the comments on the post
4. We use the django model form, since we will br writing to our database
5. Our modelform takes parameters model = comment and fields = name, email and body
6. model = Comment..uses the fields of the Comment model to generate our comment form
"""


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')



