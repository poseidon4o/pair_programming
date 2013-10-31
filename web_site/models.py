
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Pair(models.Model):
    name = models.CharField(max_length=50)
    task = models.CharField(max_length=250)
    lang = models.CharField(max_length=25)
    users = models.ManyToManyField(User, related_name='users')
    turn = models.OneToOneField(User, related_name='turn')
    owner = models.OneToOneField(User, related_name='owner')

    @models.permalink
    def get_absolute_url(self):
        return 'web_site.views.pair', [str(self.id)]

    def is_user_in(self, user_id):
        for u in self.users.all():
            if u.id == user_id:
                return True
        return False

    def has_free_spot(self):
        return len(self.users.all()) < 2

    def push_user(self, user):
        self.users.add(user)

    def pop_user(self, user):
        self.users.remove(user)
        if self.users.count() < 1:
            self.delete()

    def get_context(self):
        return {'pair': self}

    def __unicode__(self):
        return self.name