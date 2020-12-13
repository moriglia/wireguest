from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Peer


@login_required
def home(request):
    context = {
        'peers': Peer.objects.filter(user=request.user),
        'username': request.user.username
    }
    return render(request, 'keygenerator/user_keys.html', context)
