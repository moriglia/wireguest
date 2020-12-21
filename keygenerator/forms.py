from django import forms


class InterfaceForm(forms.Form):
    interface_name = forms.CharField(label="Interface name", max_length=20)
    interface_public_key = forms.RegexField(
        label="Public Key",
        regex="^[a-zA-Z0-9+/]{43}=$",
        max_length=44,
        min_length=44
    )
