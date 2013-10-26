
from django.db import models
from django.contrib.auth.models import User


class Pair(models.Model):
    name = models.CharField(max_length=50)
    task = models.CharField(max_length=50)
    lang= models.CharField(max_length=25)
    l_u_id = models.ForeignKey(User, related_name='left_user_id')
    r_u_id = models.ForeignKey(User, related_name='right_user_id')
    turn = models.CharField(max_length=10)  # left or right

    @models.permalink
    def get_absolute_url(self):
        return 'pair', self.id