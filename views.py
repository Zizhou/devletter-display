from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from submit.models import Game, Developer
from display.models import Letter, UserProfile

import re #fucking regex


# Create your views here.

@login_required
def main_page(request):
    return render(request, 'display/main_page.html')

@login_required
def devlist(request):
    
    context = {
        'devlist' : Developer.objects.all().order_by('name')
    }
    return render(request, 'display/devlist.html', context)

@login_required
def gamelist(request):
    context = {
        'gamelist' : Game.objects.all().order_by('name')
    }
    return render(request, 'display/gamelist.html', context)

@login_required
def queue(request):
    return render(request, 'display/myqueue.html')

#indivual dev page listing all associated games
#also links to letter writing page
#dynamic!
@login_required
def profile(request, dev_id):
    devname = get_object_or_404(Developer.objects.filter(id = dev_id))
    gamelist = Game.objects.filter(developer_id = dev_id).order_by('name')
    context = {
    'developer' : devname.name,
    'gamelist' : gamelist,
    }
    return render(request, 'display/profile.html', context)

#user profile page, moved here, since it's also doubling as the personal queue
#kinda jank, to be honest
@login_required
def user_profile(request):
    username = request.user.username
    #this is so gonna fail at some point...
    user_profile = UserProfile.objects.filter(user_id = request.user.id)[0]
    #...and if that doesn't, this surely will
    if request.method == 'POST':
        if request.POST.get('sig-change'):
            user_profile.signature = request.POST.get('sig_change')
            user_profile.save()
        for i in request.POST:
            print 'developer_id is: ' + i
            removeme = re.match(r'(remove_)(?P<dev_id>[0-9]+)', i)
            if removeme:
                dev_id = int(removeme.group('dev_id'))
                user_profile.devlist.remove(Letter.objects.filter(id = dev_id)[0])
            user_profile.save()
 

    sig = user_profile.signature

    #what's it being ordered by? who knows!
    #like, seriously, I'm not 100% on this syntax...
    #raw table name? probably?
    queue = user_profile.devlist.all().exclude(written = True).order_by('developer__name')
    context = {
        'name' : username,
        'sig' : sig,
        'queue' : queue
    }
    return render(request, 'display/user_profile.html', context)
