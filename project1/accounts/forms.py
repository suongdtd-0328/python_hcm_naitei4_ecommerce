import re
from django import forms
from .models import Account
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Enter password')
    }), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Confirm password')
    }), required=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = _(
            'Enter first name')
        self.fields['last_name'].widget.attrs['placeholder'] = _(
            'Enter last name')
        self.fields['phone_number'].widget.attrs['placeholder'] = _(
            'Enter phone number')
        self.fields['email'].widget.attrs['placeholder'] = _('Enter email')
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'\b[\w.-]+@[\w.-]+\.\w{2,4}\b', email):
            raise forms.ValidationError('Invalid email format!')
        if Account.objects.filter(email=email).exists():
            raise ValidationError('Email already exists!')
        return email

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                _('Password does not match!')
            )
