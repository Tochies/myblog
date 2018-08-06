from django.contrib import admin
from .models import Post, Comment

"""
1. By default, using the "contrib.auth.model import User", the User is registered in the django admin
2. We register the Post model to show on the admin site
3. We can customize the way models are displayed on the admin site by creating a PostAdmin class with
    list_display options to show the model fiels to be shown in the list
    list_filter options to show the properties used to filter posts
    search_fields options that will be used for search of posts on the admin site
    raw_id_fields with author
    prepopulated_fields options is used to tell django to populate the slug field using the post title
4. We register the comment model in like manner as the post model
"""


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title','body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)


# Register the comments in the admin section
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)