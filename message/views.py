from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from users.models import User

from .forms import MessageForm
from .models import Message


class MessageCreateView(CreateView):
    form_class = MessageForm
    template_name = 'message/message_create.html'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = User.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message
    template_name = 'message/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        return super().get_queryset().select_related('sender', 'receiver')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['message'].receiver == self.request.user:
            context['message'].unread = False
            context['message'].save()
        return context


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'message/message_update.html'
    fields = ["title", "text"]


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message/message_delete.html'
    success_url = reverse_lazy('message_list', kwargs={"folder": "inbox"})


class MessageListView(ListView):
    model = Message
    template_name = 'message/message_list.html'
    context_object_name = 'messages'
    paginate_by = 2

    def get_queryset(self):
        user = self.request.user
        if self.kwargs['folder'] == 'sent':
            return Message.objects.filter(sender=user).select_related('sender', 'receiver').order_by('-created_at')
        messages = Message.objects.filter(receiver=user).select_related('sender').order_by('-created_at')
        return messages

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder'] = self.kwargs['folder']
        return context
