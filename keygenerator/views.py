from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return HttpResponse(content="Authenticated")
