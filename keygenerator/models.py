from django.db import models
from django.contrib.auth.models import User
from .fields import IPv4AddressField
from django.utils import timezone


class Peer(models.Model):
    name = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = IPv4AddressField()
    public_key = models.CharField(max_length=44)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Peer(user={self.user} address={self.address} "\
            f"pub_key={self.public_key} created={self.creation_date})"
