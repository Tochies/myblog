from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post       # We use .. to navigate two folders

"""
1. So we can use the tags in our html pages in cases like {% total_posts %}
2. A simple tag just returns a value
3. In our inclusion tag (latest_posts), we specify the template to render, inclusion tags have to return a dictionary of values to be used in the context
4. An inclusion tag uses a template to generate list
5. We remove the assignment tag, since it is now deprecated since django 1.9, simple tag does the job
6. We now use a simple tag to get the most commented post
7. We use marksafe and markdown to truncate words to a certain number of words
"""
register = template.Library()


# We defined a simple tag to get the total post published
@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag()
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
