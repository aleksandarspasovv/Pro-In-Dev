from django.urls import path
from ProInDev.messages_app.views import messaging_view, send_message_view

app_name = 'messages_app'

urlpatterns = [
    path('', messaging_view, name='messaging'),
    path('send/', send_message_view, name='send_message'),
]
