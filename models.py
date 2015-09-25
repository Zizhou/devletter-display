from django.db import models
from django import forms

from django.db.models.signals import post_save

from submit.models import Game, Developer
from django.contrib.auth.models import User

import datetime
# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length = 100)
    template = models.TextField(blank = True)
    subject = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.name

class Letter(models.Model):
    developer = models.ForeignKey(Developer)
    #one game per dev?
    game = models.ForeignKey(Game, null = True)
    written = models.BooleanField(default = False)
    #probably the only thing anyone will fill out
    text1 = models.TextField(blank = True)
    #future proofing because I'm too lazy to figure out a better way
    text2 = models.TextField(blank = True)
    template = models.ForeignKey(Template, null = True) 
    subject = models.CharField(max_length = 200, blank = True)

    def __unicode__(self):
        return self.developer.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique = True)
    devlist = models.ManyToManyField(Letter, blank = True)
    signature = models.CharField(max_length = 100, blank = True)
##the following are for automatic code distribution
    ticket_count = models.IntegerField(default = 0)
    last_donation = models.DateTimeField(default = datetime.datetime(1970, 1,1,0,0,0),blank = True)
    donation_count = models.IntegerField(default = 0)
    
    class Meta:
        permissions = (
            ('write_letter', 'Can write letters'),
        )

    def __unicode__(self):
        return self.user.username
    
    def ticket_decrement(self, val):
        if self.ticket_count - val < 0:
            return False
        self.ticket_count -= val
        self.save()
        return True
 
    def ticket_increment(self, val):
        self.ticket_count += val
        self.save()
        return True
    #on donation, update count, returns true if last donation was >1 hour ago
    def donation_update(self):
        self.donation_count += 1
        donation_delta = self.last_donation + datetime.timedelta(0,3600)
        donation_delta = donation_delta.replace(tzinfo = None)
        self.last_donation = datetime.datetime.now()
        self.save()
        print donation_delta
        print self.last_donation
        if donation_delta < self.last_donation:
            return True
        else: 
            return False

class TemplateSelectForm(forms.ModelForm):
    template = forms.ModelChoiceField(queryset = Template.objects.all().order_by('id'), initial = 1, empty_label = None, widget = forms.RadioSelect)
    class Meta:
        model = Letter
        fields = ['template']


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
#updates default game in letter (and template) whenever a new game is added to a dev
def letter_game_update(sender, instance, created, **kwargs):
    l = Letter.objects.get(developer = instance.developer)
    l.game = instance
    ##slightly lazy
    #if instance.lastyear:
    #    l.template = Template.objects.get(name = 'Replay')
    #else:
    #    l.template = Template.objects.get(name = 'New Contact')
    l.save()

post_save.connect(letter_create, sender = Developer)
post_save.connect(letter_game_update, sender = Game)
