from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
"""
Here in this case, we use the django user model to associate users that post and can comment on the blog
1. Posts can either be draft or published status...the default post status is draft..this is achieved using the django choices option
2. We use the django timezone.now for getting the current time of post publish
3. Each post has the following fields [title, slug, body(text), author, publish, created, updated, status]
4. The post model has STATUS_CHOICES which will be used for the django choices option in the status using CharField
5. We use a Meta class to set the ordering of the post published to be the latest posts
6. The __str__ function is used to return a human readable title for the post, which will be used for the database and admin
7. By default, we use the django object manager to create, update, delete and save model object(can also be done using the admin site)
8. To enable us use say only published posts, we can create a custom model manager, which uses the models.Manager class
    an example of such here is the custom PublishedManager class,
    hence the objects and published of our Post class, so we can now perform queries like
    Post.published.all or Post.published.filter(title__startswith='who') on our query commands
9. We define the "get_absolute_url" function to tell django to create canonical(general) url for the views
10. We define the comments model in its own class
11. We associate each comment to a post, using a foreignkey
12. Note, anyone can comment on the post without being a registered user, since we did not attach user validation to comment
13. We return a human readable string of name and post commented for use in database and admin site
"""

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # canonical url for the post_detail view, which checks for the year,month,day and slug of post
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'), self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)








