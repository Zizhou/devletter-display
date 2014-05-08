from django.db import models

from django.db.models.signals import post_save

from submit.models import Game, Developer
from django.contrib.auth.models import User

# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length = 100)
    template = models.TextField(blank = True)

    def __unicode__(self):
        return self.name

class Letter(models.Model):
    developer = models.ForeignKey(Developer)
    #one game per dev?
    game = models.ForeignKey(Game, null = True)#, limit_choices_to={'developer_id':developer.id)
    written = models.BooleanField(default = False)
    #probably the only thing anyone will fill out
    text1 = models.TextField(blank = True)
    #future proofing because I'm too lazy to figure out a better way
    text2 = models.TextField(blank = True)
    template = models.ForeignKey(Template, null = True)    

    def __unicode__(self):
        return self.developer.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique = True)
    devlist = models.ManyToManyField(Letter, blank = True)
    
    signature = models.CharField(max_length = 100, blank = True)
    
    class Meta:
        permissions = (
            ('write_letter', 'Can write letters'),
        )    

    def __unicode__(self):
        return self.user.username

def user_profile_create(sender, instance, created, **kwargs):
    if created == True:
        u = UserProfile()
        u.user = instance
        u.save()

post_save.connect(user_profile_create, sender = User)

def letter_create(sender, instance, created, **kwargs):
    if created == True:
        l = Letter()
        l.developer = instance
        l.save()

post_save.connect(letter_create, sender = Developer)
