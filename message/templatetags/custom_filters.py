from django import template
from message.models import Message

register = template.Library()


@register.filter
def unread_message_count(user):
    return Message.objects.filter(receiver=user, unread=True).count()
