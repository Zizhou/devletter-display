from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from submit.models import Game, Developer
from display.models import Letter, UserProfile, TemplateSelectForm

import re #fucking regex


# Create your views here.

@login_required
def main_page(request):
    #this is so gonna fail at some point...
    user_profile = UserProfile.objects.filter(user_id = request.user.id)[0]
    #...and if that doesn't, this surely will
    if request.method == 'POST':
        for i in request.POST:
            print i
            addme = re.match(r'(add_)(?P<dev_id>[0-9]+)', i)
            if addme:
                dev_id = int(addme.group('dev_id'))
                user_profile.devlist.add(Letter.objects.filter(id = dev_id)[0])
            user_profile.save()
 

    queue = Letter.objects.exclude(written = True).order_by('developer__name')
    context = {
        'queue' : queue
    }
    return render(request, 'display/main_page.html', context)

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

#indivual dev page listing all associated games
#also links to letter writing page
#dynamic!
@login_required
def profile(request, dev_id):
    devname = get_object_or_404(Developer.objects.filter(id = dev_id))
    gamelist = Game.objects.filter(developer_id = dev_id).order_by('name')
    letter_id = Letter.objects.get(developer_id = dev_id).id 
    context = {
    'developer' : devname.name,
    'gamelist' : gamelist,
    'letter_id': letter_id,
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
        if request.POST.get('sig_change'):
            user_profile.signature = request.POST.get('sig_change')
            user_profile.save()
        for i in request.POST:
            removeme = re.match(r'(remove_)(?P<dev_id>[0-9]+)', i)
            if removeme:
                dev_id = int(removeme.group('dev_id'))
                user_profile.devlist.remove(Letter.objects.filter(id = dev_id)[0])
            user_profile.save()
 
    tickets = user_profile.ticket_count

    sig = user_profile.signature

    #what's it being ordered by? who knows!
    #like, seriously, I'm not 100% on this syntax...
    #raw table name? probably?
    queue = user_profile.devlist.exclude(written = True).order_by('developer__name')
    context = {
        'name' : username,
        'sig' : sig,
        'queue' : queue,
        'ticket_count' : tickets,
    }
    return render(request, 'display/user_profile.html', context)

def bulk_template(request):
    error = []
    if request.method =='POST':
        for x in Letter.objects.all().order_by('developer__name'):
            form = TemplateSelectForm(request.POST, instance = x, prefix = x.developer)
            if form.is_valid():
                try:
                    form.save()
                except:
                    try:
                        error.append(x.developer.name.decode('utf-8'))
                    except:
                        error.append(unicode(x.id)+'this one\'s funny...')

    form = []
    for x in Letter.objects.all().order_by('developer__name'):
        form.append({'name':x.developer.name, 'form':TemplateSelectForm(instance = x, prefix = x.developer)})

    context = {
        'forms':form,
        'error' : error,
        'message' : len(error)>0
    }
    return render(request, 'display/bulk_template.html', context)
