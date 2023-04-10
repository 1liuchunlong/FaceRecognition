from django.urls import re_path

from App import consumers

websocket_urlpatterns = [
    re_path(r'face/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
