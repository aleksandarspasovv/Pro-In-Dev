from django.db.models import Max, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ProInDev.messages_app.models import Message
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def messaging_view(request):
    chat_user = None
    messages = None

    latest_messages = (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .annotate(latest_id=Max('id'))
        .order_by('-timestamp')
    )

    chat_partners = {}
    for message in latest_messages:
        if message.sender == request.user:
            partner = message.receiver
        else:
            partner = message.sender
        if partner not in chat_partners or chat_partners[partner].timestamp < message.timestamp:
            chat_partners[partner] = message

    latest_messages = sorted(chat_partners.values(), key=lambda x: x.timestamp, reverse=True)

    if 'chat' in request.GET:
        chat_user_id = request.GET.get('chat')
        try:
            chat_user = User.objects.get(id=chat_user_id)
            messages = Message.objects.filter(
                Q(sender=request.user, receiver=chat_user)
                | Q(sender=chat_user, receiver=request.user)
            ).order_by('timestamp')
        except User.DoesNotExist:
            chat_user = None

    return render(request, 'messaging.html', {
        'chat_user': chat_user,
        'messages': messages,
        'latest_messages': latest_messages,
    })


# @login_required
# def send_message_view(request):
#     if request.method == 'POST':
#         receiver_id = request.POST.get('receiver')
#         content = request.POST.get('content')
#
#         try:
#             receiver = User.objects.get(id=receiver_id)
#             Message.objects.create(sender=request.user, receiver=receiver, content=content)
#         except User.DoesNotExist:
#             pass
#
#     return redirect('messages_app:messaging')


def send_message_view(request, user_id):
    if request.method == "POST":
        receiver = get_object_or_404(User, id=user_id)
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, "Message sent successfully.")
        else:
            messages.error(request, "Message cannot be empty.")
        return redirect("messages_app:messaging")

    receiver = get_object_or_404(User, id=user_id)
    return HttpResponseRedirect(f"/messages/?chat={receiver.id}")
