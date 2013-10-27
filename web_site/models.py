
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Pair(models.Model):
    name = models.CharField(max_length=50)
    task = models.CharField(max_length=50)
    lang= models.CharField(max_length=25)
    l_u_id = models.PositiveIntegerField(null=True)
    r_u_id = models.PositiveIntegerField(null=True)
    turn = models.CharField(max_length=10)  # left or right

    @models.permalink
    def get_absolute_url(self):
        return ('web_site.views.pair', [str(self.id)])


    def __unicode__(self):
        return self.name