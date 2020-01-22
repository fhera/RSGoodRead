# -*- encoding: utf-8 -*-
from django import forms


class UserForm(forms.Form):
    id_usuario = forms.IntegerField(
        label="id_usuario",
        widget=forms.TextInput,
        required=True
    )


class BookForm(forms.Form):
    id = forms.CharField(label='Book ID')
