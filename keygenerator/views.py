# SPDX-License-Identifier: GPLv3-or-later
# Copyright (C) 2020 Marco Origlia

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Peer
from .forms import InterfaceNameForm
from .peer_interface_registration import registrate_interface
from django.contrib import messages


@login_required
def home(request):
    context = {
        'peers': Peer.objects.filter(user=request.user),
        'username': request.user.username
    }
    return render(request, 'keygenerator/user_keys.html', context)


@login_required
def create_peer_interface(request):
    if request.method == "POST":
        form = InterfaceNameForm(request.POST)
        if form.is_valid():
            interface_name = form.cleaned_data['interface_name']
            ip = registrate_interface(request.user, interface_name)
            if ip:
                messages.success(
                    request,
                    f"Created a new interface {interface_name} with ip {ip} "
                    f"for user {request.user.username}"
                )
            else:
                messages.error(
                    request,
                    f"Unable to create interface {interface_name} for "
                    "{request.user.username}"
                )

            return redirect('keygen-home')
        else:
            messages.error(request, "Invalid name for interface")

    form = InterfaceNameForm()

    return render(
        request,
        'keygenerator/create_peer_interface.html',
        {
            'form': form,
            'user': request.user.username
        }
    )
