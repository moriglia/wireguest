from django import forms


class InterfaceNameForm(forms.Form):
    interface_name = forms.CharField(label="Interface name", max_length=20)
