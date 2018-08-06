from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
# the post list view is the same as the classBased view of PostListView
"""
1. We use the django shortcut to render our pages to the browser, this results in the page or a 404 error message
2. Since, we want to display all(published) of our posts, we import the Post model
3. Note all views take the request object as a parameter, which is to request and render urls
4. We use django's builtin paginator module to auto make nex page when a particular page is full
5. We render our context list in hierarchy of sequence of page display~~~page, post, tag
6. It is important for each context to be unique
7. We create a view to share posts
8. We add comment parameters to our post detail view..This is so because, we need display comments for individual posts
9. Rendering our comments from the view follows the same procedures as the email, since both are forms


"""

# We use the post_list view to render two url patterns... for general post list and for post ist by tags


def post_list(request, tag_slug=None):
    # This returns all the published posts
    object_list = Post.published.all()
    # the default post tag is none
    tag = None

    # This is used to render list of posts with similar tags
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # This populates the page with 3 pages per page
    paginator = Paginator(object_list, 3)  # for 3 posts per page
    # This requests for the page.NB: 'page' is the default syntax for paginator request.get
    page = request.GET.get('page')
    try:
        # returns the page requested
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        # we render the page with its contexts, we
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


'''
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
'''


def post_detail(request, year, month, day, post, tag_slug=None):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments,this is used for the context to show active posts on the webpage
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment but dont save it yet to the database
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # list of tags, since we will be calling all the post with similar tags, we get all the published posts
    object_list = Post.published.all()
    # The default tag for each post is None
    tag = None

    # the tag_slug is defined as an optional parameter for the post_detail view
    # This tag_slug is used to update the object_list, by filtering only post with the same tags
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # List of similar posts
    # we use tags to get posts with similar tags
    # values_list is a queryset which returns tuples for the given "id" field, setting it flat, brings a list like [1,2,..]
    post_tags_ids = post.tags.values_list('id', flat=True)
    # we get all the similar post, excluding the post we are currently viewing
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # We display recent posts first for posts with same tags as current post
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form,  'similar_posts': similar_posts,'tag': tag})


# Here we create view for sharing our post, the post will be shared using its unique id
# Here we use the GET method to get the initial form and use the POST method to validate and submit the form
# By default post_share is not rendered, until its clicked on the post detail template

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    # We set the initial status of the share to be false
    sent = False

    # When the view is loaded, the else statement renders the empty form using GET method for the first time
    # If the form is filled, the if request.method sends the form details as POST method
    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            #....send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # This sends the subject and extra message alongside the post using name,email and comments from the form class
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            # Here we use the send_mail class from the django mail module to send the post via email
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post': post, 'form': form, 'sent': sent})

























