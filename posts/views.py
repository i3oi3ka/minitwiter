from comment.models import Comment
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import DeleteView

from .forms import PostForm
from .models import Post


# def posts_list(request, user_id=None):
#     comment_count = dict()
#     if user_id:
#         posts = Post.objects.filter(user__id=user_id)
#     else:
#         posts = Post.objects.all()
#     if posts:
#         for post in posts:
#             comment_count[str(post.pk)] = Comment.objects.filter(post__id=post.pk).count()
#     return render(request, 'posts/posts_list.html', {'posts': posts, 'comment_count': comment_count})

# перевірка чи запит було здійснено з нашого домену!
def is_valid_request(request):
    allowed_origin = "http://127.0.0.1"
    origin = request.headers.get("Origin") or request.headers.get("Referer")
    if origin.startswith(allowed_origin):
        return True
    return False


class PostListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.kwargs.get('folder'):
            folder = self.kwargs.get('folder')
            if folder == 'my':
                posts = Post.objects.filter(user=self.request.user).select_related('user')
            elif folder == 'follow':
                follow_users = self.request.user.following.all()
                posts = Post.objects.filter(user__in=follow_users).select_related('user')
        else:
            posts = Post.objects.all().select_related('user')
        return posts.annotate(comment_count=Count('comment', distinct=True),
                              like_count=Count('like', distinct=True)).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('folder'):
            context['folder'] = self.kwargs['folder']
        else:
            context['folder'] = 'all'

        return context


class PostUserListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        posts = Post.objects.filter(user__id=self.kwargs['user_id']).select_related('user')
        return posts.annotate(comment_count=Count('comment', distinct=True),
                              like_count=Count('like', distinct=True)).order_by('-created_at')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     follow_users = user.following.all()
    #     context['posts'] = context['posts'].filter(user__in=follow_users).select_related('user').annotate(
    #         comment_count=Count('comment', distinct=True),
    #         like_count=Count('like', distinct=True)).order_by('-created_at')
    #     return context


# def get_context_data(self, *, object_list=None, **kwargs):
#     context = super().get_context_data(**kwargs)
#     comment_count = dict()
#     if context['posts']:
#         comment_count = Comment.objects.values('id')
#     context['comment_count'] = comment_count
#     return context


# def comments_list(request, post_id):
#     comments = Comment.objects.filter(post__id=post_id)
#     post = get_object_or_404(Post, pk=post_id)
#     context = {
#         'comments': comments,
#         'post': post
#     }
#     return render(request, 'posts/comments_list.html', context)


# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save()
#             return redirect('post_detail', post_id=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'posts/create_post.html', {'form': form})

class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        if is_valid_request(self.request):
            form.instance.user = self.request.user  # Передаємо користувача
            return super().form_valid(form)
        else:
            return HttpResponse(f"Go to Hell")


# def post_detail(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     comments = Comment.objects.filter(post__id=post_id)
#     context = {"post": post, 'count_comments': len(comments), 'comments': comments}
#     return render(request, "posts/post_detail.html", context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_queryset(self):
        post = super().get_queryset()
        return post.select_related('user').annotate(comment_count=Count('comment', distinct=True),
                                                    like_count=Count('like', distinct=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post__id=self.kwargs['pk']).select_related('user').order_by(
            '-created_at')
        return context


class PostUpdateView(UpdateView):
    template_name = 'posts/post_update.html'
    model = Post
    fields = ["title", "image", "content"]

    def get_queryset(self):
        return super().get_queryset().select_related('user')


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('posts_list')
    template_name = 'posts/post_delete.html'


# def create_comment(request):
#     if request.method == 'POST':
#        form = CommentForm(request.POST, request.FILES)
#        if form.is_valid():
#             comment = form.save()
#             return redirect('comment_detail', comment_id=comment.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'posts/create_comment.html', {'form': form})


def like(request, pk):
    post = Post.objects.get(pk=pk)
    post.like.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LikedPostUserList(ListView):
    model = Post
    template_name = 'posts/liked_post_user.html'
    context_object_name = 'post_liked_user'

    def get_queryset(self):
        post_liked_user = Post.objects.get(pk=self.kwargs['pk']).like.all()
        return post_liked_user
