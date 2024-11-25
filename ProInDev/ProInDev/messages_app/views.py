from django.db.models import Max, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ProInDev.messages_app.models import Message
from django.contrib.auth.models import User


@login_required
def messaging_view(request):
    chat_user = None
    messages = None

    latest_messages = (
        Message.objects.filter(receiver=request.user)
        .values('sender')
        .annotate(latest_id=Max('id'))
    )

    latest_message_ids = [item['latest_id'] for item in latest_messages]
    latest_messages = Message.objects.filter(id__in=latest_message_ids).order_by('-timestamp')

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

    users = User.objects.exclude(id=request.user.id)

    return render(request, 'messaging.html', {
        'chat_user': chat_user,
        'messages': messages,
        'latest_messages': latest_messages,
        'users': users,
    })


@login_required
def send_message_view(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')

        try:
            receiver = User.objects.get(id=receiver_id)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
        except User.DoesNotExist:
            pass

    return redirect('messages_app:messaging')
