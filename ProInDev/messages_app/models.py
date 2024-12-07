from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):  # Model to represent a message
    sender = models.ForeignKey(  # Sender of the message
        to=User,
        on_delete=models.CASCADE,  # Deletes messages if the user is deleted
        related_name='sent_messages'  # Related name for reverse query
    )

    receiver = models.ForeignKey(  # Receiver of the message
        to=User,
        on_delete=models.CASCADE,  # Deletes messages if the user is deleted
        related_name='received_messages'  # Related name for reverse query
    )

    content = models.TextField()  # Content of the message

    timestamp = models.DateTimeField(  # Timestamp of when the message was sent
        auto_now_add=True,  # Automatically set to now when created
    )

    is_read = models.BooleanField(  # Whether the message has been read
        default=False,  # Default value is unread
    )

    def __str__(self):  # String representation of the message
        return f'From {self.sender.username} to {self.receiver.username}'
