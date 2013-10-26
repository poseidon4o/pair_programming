from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class User(User.objects):
    def join_pair(self, Pair):
        Pair.l_u_id = self.id
        return Pair

class Pair(models.Model):
    pairname = models.CharField(max_length=50)
    task = models.CharField(max_length=50)
    prog_language = enumerate('C', 'C++', 'C#', 'Python', 'PHP', 'HTML', 'Java')
    l_u_id = models.ForeignKey(User)
    r_u_id = models.ForeignKey(User)

    def set_details(self, pairname, task, prog_language):
        self.task = task
        self.pairname = pairname
        self.prog_language = prog_language

    def join_user(self, User):
        self.r_u_id = User.id