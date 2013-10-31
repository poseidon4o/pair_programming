from django.contrib import auth
from web_site.models import Pair
import logging
logger = logging.getLogger(__name__)


class ContextManager:
    CHANNEL_PREFIX = 'pair-code-'
    pair = None
    user = None

    def __init__(self, ctx, request, channel=None):
        if ctx.get('usr_count') is None:
            ctx['usr_count'] = 0
        self.ctx = ctx
        self.chnl = channel
        self.rq = request
        self._test_usr()
        self._parse_channel()

    def _can_message(self):
        return self.user is not None and \
            self.ctx.get(self.user.id) is not None and \
            self.ctx[self.user.id]['pair'] is not None and \
            self.ctx[self.user.id]['pair'].users.filter(id=self.user.id).exists() and \
            self.ctx[self.user.id]['pair'].turn.id == self.user.id


    def _parse_channel(self):
        if self.chnl is None and self.ctx.get(self.user.id):
            self.chnl = self.ctx[self.user.id]['channel']

        if self.chnl is not None and len(self.chnl[len(self.CHANNEL_PREFIX):]):
            self.pair = Pair.objects.get(id=self.chnl[len(self.CHANNEL_PREFIX):])
            if self.pair is None:
                logger.debug('ContextManager: Can\'t load pair from channel.')
                raise Exception('Can\'t load pair from channel')

    def _test_usr(self):
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

    def m_message(self, msg):
        logger.debug('ContextManager: message')
        if self.user is not None and self._can_message() and msg.get('data'):
            return msg['data']
        return ''

    def m_internal_message(self, msg):
        pass
