from django_socketio import events
from web_site.context_manager import ContextManager
import logging
logger = logging.getLogger(__name__)


@events.on_connect
def connect(request, socket, context):
    try:
        cm = ContextManager(context, request)
        cm.m_connect()
    except:
        pass


@events.on_subscribe(channel='^' + ContextManager.CHANNEL_PREFIX)
def subscribe(request, socket, context, channel):
    try:
        cm = ContextManager(context, request, channel)
        cm.m_subscribe()
    except:
        pass


@events.on_unsubscribe(channel='^' + ContextManager.CHANNEL_PREFIX)
def unsubscribe(request, socket, context, channel):
    try:
        cm = ContextManager(context, request, channel)
        cm.m_unsubscribe()
    except:
        pass


@events.on_disconnect
def disconnect(request, socket, context):
    try:
        cm = ContextManager(context, request)
        cm.m_disconnect()
    except:
        pass


@events.on_finish
def finish(request, socket, context):
    # not sure when this is called
    logger.debug('FINISH')


@events.on_message(channel="^pair-code-")
def message(request, socket, context, message_obj):
    try:
        cm = ContextManager(context, request)
        if message_obj.get('_internal_command'):
            cm.m_internal_message(message_obj)
        else:
            cm.m_message(message_obj)
    except:
        pass
