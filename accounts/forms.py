# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from accounts.models import Account, Balance
from .models import WalletAddress


class RegistrationForm(UserCreationForm):
    fullname = forms.CharField(max_length=100, help_text='Required. Enter your full name')
    email = forms.EmailField(max_length=100, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ("fullname", "username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.fullname = self.cleaned_data['fullname']
        user.phone = 'Not set'
        user.country = 'Not set'
        if commit:
            user.save()
            Balance.objects.create(user=user)
        return user

class AccountAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            cleaned_data = super().clean()
            email = cleaned_data.get("email")
            password = cleaned_data.get("password")
            if email and password:
                user = authenticate(email=email, password=password)
                if not user:
                    raise forms.ValidationError('Invalid login credentials')
            return cleaned_data



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'phone', 'country']

    def clean_username(self):
        username = self.cleaned_data['username']
        if Account.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Username already taken. Please choose a different username.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Email already taken. Please choose a different email.')
        return email


class ContactForm(forms.Form):
    email = forms.EmailField(label='Your Email Address', required=True)
    subject = forms.CharField(label='Subject', max_length=100, required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea, required=True)

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['profile_picture']                



class WalletAddressForm(forms.ModelForm):
    class Meta:
        model = WalletAddress
        fields = ['wallet_type', 'address']  
     
        
        