from django.db.models import Max, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ProInDev.messages_app.models import Message
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def messaging_view(request):  # View for the messaging interface
    chat_user = None  # The user currently being chatted with
    messages = None  # The messages in the current chat

    # Get the latest message for each chat involving the current user
    latest_messages = (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .annotate(latest_id=Max('id'))
        .order_by('-timestamp')
    )

    chat_partners = {}  # Dictionary to store the latest message per chat partner
    for message in latest_messages:
        if message.sender == request.user:
            partner = message.receiver  # Identify the chat partner
        else:
            partner = message.sender
        # Update the latest message for the chat partner
        if partner not in chat_partners or chat_partners[partner].timestamp < message.timestamp:
            chat_partners[partner] = message

    # Sort the latest messages by timestamp, most recent first
    latest_messages = sorted(chat_partners.values(), key=lambda x: x.timestamp, reverse=True)

    if 'chat' in request.GET:  # If a specific chat is requested
        chat_user_id = request.GET.get('chat')
        try:
            chat_user = User.objects.get(id=chat_user_id)  # Get the chat user
            # Retrieve messages between the current user and the chat user
            messages = Message.objects.filter(
                Q(sender=request.user, receiver=chat_user)
                | Q(sender=chat_user, receiver=request.user)
            ).order_by('timestamp')
        except User.DoesNotExist:
            chat_user = None  # If the user doesn't exist, set chat_user to None

    return render(request, 'messaging.html', {  # Render the messaging template
        'chat_user': chat_user,
        'messages': messages,
        'latest_messages': latest_messages,
    })


@login_required
def send_message_view(request, user_id):  # View to handle sending a message
    if request.method == "POST":  # Only handle POST requests
        receiver = get_object_or_404(User, id=user_id)  # Get the recipient
        content = request.POST.get('content', '').strip()  # Get and strip the message content
        if content:
            # Create the message if the content is not empty
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, "Message sent successfully.")
        else:
            messages.error(request, "Message cannot be empty.")
        return redirect("messages_app:messaging")  # Redirect to the messaging interface

    receiver = get_object_or_404(User, id=user_id)  # If not a POST request, redirect to the chat
    return HttpResponseRedirect(f"/messages/?chat={receiver.id}")
