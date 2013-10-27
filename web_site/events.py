
from django.shortcuts import get_object_or_404
from django_socketio import events

from web_site.models import Pair


@events.on_connect
def connect(request, socket, context):

    print "connect"


@events.on_message(channel="^pair-code-")
def message(request, socket, context, message):
    """
    Event handler for pair data channel
    """
    socket.send_and_broadcast_channel({'code': message['code']})
    if 'pair_id' not in message or 'user_id' not in message:
        return

    pair = get_object_or_404(Pair, id=message['pair_id'])

    if pair.l_u_id != int(message['user_id']) and pair.r_u_id != int(message['user_id']):
        return

