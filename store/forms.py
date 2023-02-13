from django.contrib.auth import password_validation

from django import forms
import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _
from .models import *


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    email = forms.CharField(required=True,
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    rationcardno = forms.CharField(required=True,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'RationCard No'}))

    class Meta:
        model = User
        fields = ['username', 'rationcardno', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})}


class LoginForm(AuthenticationForm):
    # print('))))))))))))))))))))))))')
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

    # print('----',username)
    # print('----',password)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Customerdetails
        fields = ['locality', 'city', 'mobno', 'email', 'rationcardno', 'rationcardphoto']
        widgets = {'locality': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Popular Place like Restaurant, Religious Site, etc.'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'mobno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobno'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
            'rationcardno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'rationcardno'})
        }


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'auto-focus': True, 'class': 'form-control',
               'placeholder': 'Current Password'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'New Password'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Confirm Password'}))


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class addproductform(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class addstockform(forms.ModelForm):
    class Meta:
        model = stock
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(addstockform, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class dailreportform(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = '__all__'


class StaffUpdateorderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        STATUS_CHOICES = (
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Packed', 'Packed'),
            ('On The Way', 'On The Way'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled')
        )
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES, attrs={'class': 'form-control'}),
        }


class ReviewAdd(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('review_text', 'review_rating')

        RATING = (
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        )
        widgets = {
            'review_rating': forms.Select(choices=RATING, attrs={'class': 'form-control'}),
        }
