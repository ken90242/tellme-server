from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from messenger.consumers import MessageConsumer
from notifications.consumers import NotificationsConsumer

from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

import urllib.parse
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query_string = scope['query_string']
        if query_string:
            try:
                qs_dict = urllib.parse.parse_qs(query_string)
                print(query_string)
                if qs_dict[b'token']:
                    print(qs_dict[b'token'])
                    jwt = qs_dict[b'token'][0]
                    print(jwt)
                    decoded_payload = jwt_decode_handler(jwt)
                    user = User.objects.filter(username=decoded_payload['username'])
                    if user:
                        scope['user'] = user[0]
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        return self.inner(scope)

SJWTAuthMiddleware = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))

APPLICATION = ProtocolTypeRouter({
    # http protocol will be added automatically
    'websocket': SJWTAuthMiddleware(
        URLRouter([
            re_path(r'^ws/notifications/', NotificationsConsumer), 
            path('ws/<str:username>/', MessageConsumer)
            # path('ws/<str:username>/', MessageConsumer)
        ])
    )
})
