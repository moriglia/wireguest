# SPDX-License-Identifier: GPLv3-or-later
# Copyright (C) 2020 Marco Origlia

from django.db import models
from django.contrib.auth.models import User
from .fields import IPv4AddressField
from django.utils import timezone


class Peer(models.Model):
    name = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = IPv4AddressField(unique=True)
    public_key = models.CharField(max_length=44, unique=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Peer(user={self.user} address={self.address} "\
            f"pub_key={self.public_key} created={self.creation_date})"

    @staticmethod
    def maxip():
        ip = Peer.objects.aggregate(models.Max('address'))['address__max']
        # already set to None if no Peer interface is present in database

        return ip
