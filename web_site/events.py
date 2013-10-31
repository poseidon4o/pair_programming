from django_socketio import events
from django.contrib import auth
from web_site.models import Pair
import logging
logger = logging.getLogger(__name__)


class ContextManager:
    CHANNEL_PREFIX = 'pair-code-'
    pair = None
    user = None

    def __init__(self, ctx, request, channel=None):
        self.ctx = ctx
        self.chnl = channel
        self.rq = request
        self.test_usr()
        self.parse_channel()

    def parse_channel(self):
        if self.chnl is not None and len(self.chnl[len(self.CHANNEL_PREFIX):]):
            self.pair = Pair.objects.get(id=self.chnl[len(self.CHANNEL_PREFIX):])
            if self.pair is None:
                logger.debug('ContextManager: Can\'t load pair from channel.')
                raise Exception('Can\'t load pair from channel')


    def test_usr(self):
        if not auth.user_logged_in:
            logger.debug('ContextManager: User not logged in.')
            raise Exception('User not logged in')

        user = auth.get_user(self.rq)
        if user is None:
            logger.debug('ContextManager: Can\'t load user from request.')
            raise Exception('Can\'t load user from request')
        self.user = user

    def m_subscribe(self):
        logger.debug('ContextManager: subscribe')
        if self.user is not None and self.chnl is not None:
            self.ctx[self.user.id]['channel'] = self.chnl
            self.ctx[self.user.id]['pair'] = self.pair
            if not self.pair.is_user_in(self.user.id) and self.pair.has_free_spot():
                self.pair.push_user(self.user)
            else:
                raise Exception('ContextManager: Error subscribing channel.')

    def m_unsubscribe(self):
        logger.debug('ContextManager: unsubscribe')
        if self.user is not None and self.chnl is not None:
            del self.ctx[self.user.id]['pair']
            del self.ctx[self.user.id]['channel']
            self.pair.pop_user(self.user)

    def m_connect(self):
        logger.debug('ContextManager: connect')
        if self.user is not None:
            self.ctx['usr_count'] += 1
            self.ctx[self.user.id]['object'] = self.user

    def m_disconnect(self):
        logger.debug('ContextManager: disconnects')
        if self.user is not None:
            self.ctx['usr_count'] -= 1
            pair = self.ctx[self.user.id]['pair']
            if pair is not None:
                pair.pop_user(self.user)

            del self.ctx[self.user.id]


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
    logger.debug("Context message+++++++++++++++++++++++++++++++++++++++++=")
    logger.debug(context)


    return
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
