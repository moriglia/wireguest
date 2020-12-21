# SPDX-License-Identifier: GPLv3-or-later
# Copyright (C) 2020 Marco Origlia

from django.shortcuts import render  # , redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Peer
from .forms import InterfaceForm
from .peer_interface_registration import registrate_interface
from django.contrib import messages


@login_required
def home(request):
    context = {
        'peers': Peer.objects.filter(user=request.user),
        'username': request.user.username,
        'title' : "WireGuest Home"
    }
    return render(request, 'keygenerator/user_keys.html', context)


@login_required
def create_peer_interface(request):
    if request.method == "POST":
        form = InterfaceForm(request.POST)
        if form.is_valid():
            interface_name = form.cleaned_data['interface_name']
            interface_public_key = form.cleaned_data['interface_public_key']
            ip = registrate_interface(
                request.user,
                interface_name,
                interface_public_key
            )
            if ip:
                if request.is_ajax():
                    return JsonResponse(
                        {
                            "address": str(ip)
                        },
                        status=200
                    )
                else:
                    messages.success(
                        request,
                        f"Created a new interface {interface_name} "
                        f"with ip {ip} "
                        f"for user {request.user.username}"
                    )

            elif request.is_ajax():
                return JsonResponse(
                    {
                        "error": "Unable to register interface"
                    },
                    status=400
                )
            else:
                messages.error(
                    request,
                    f"Unable to create interface {interface_name} for "
                    "{request.user.username}"
                )

        elif request.is_ajax():
            return JsonResponse(
                {
                    "error": "Invalid interface data"
                },
                status=400
            )
        else:
            messages.error(request, "Invalid interface data")

    form = InterfaceForm()

    return render(
        request,
        'keygenerator/create_peer_interface.html',
        {
            'form': form,
            'user': request.user.username,
            'title': "Create Interface"
        }
    )
