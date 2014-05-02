from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from submit.models import Game, Developer
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

def user_profile(request):
    username = 'No-Man'
    if request.user.is_authenticated():
	username = username = request.user.username
    context = {
        'name' : username
    }
    return render(request, 'display/user_profile.html', context)
