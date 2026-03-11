from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from posts.models import Post

from .models import Comment
from .forms import CommentForm


class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = 'comment/create_comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class CommentListView(ListView):
    model = Comment
    template_name = 'comment/comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        comments = Comment.objects.filter(post__id=self.kwargs['post_id']).select_related('user').order_by(
            '-created_at')
        return comments

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return context


# def comment_detail(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     context = {'comment': comment}
#     return render(request, 'posts/comment_detail.html', context)

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment/comment_detail.html'
    context_object_name = 'comment'


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/comment_update.html'
    fields = ["content"]

    def get_queryset(self):
        return super().get_queryset().select_related('user')


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'
    success_url = reverse_lazy('posts_list')
