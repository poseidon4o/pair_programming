from django_socketio import events
from django.contrib import auth
import logging
logger = logging.getLogger(__name__)


@events.on_connect
def connect(request, socket, context):
    if not auth.user_logged_in:
        logger.debug('User not logged in')
        return
    context['conected_users'].append(auth.get_user(request).id)


@events.on_subscribe(channel='^pair-code-')
def subscribe(request, socket, context, channel):
    if not auth.user_logged_in:
        logger.debug('User not logged in')
        return

    user = auth.get_user(request)
    if user.id not in context['connected_users']:
        logger.debug('User tries subscribe but not connected')

    context[channel]['users'].append(user.id)


@events.on_message(channel="^pair-code-")
def message(request, socket, context, message_obj):


    pair = context.get('pair')
    if pair is None:
        logger.debug('Pair not in context')
        return

    if message_obj['pair_id'] != pair.id:
        logger.debug('Pair id doesnt match')
        return

    if message['user_id'] not in pair.users.values('id'):
        logger.debug('User id not in pair')
        return

    socket.broadcast_channel(message=message)
