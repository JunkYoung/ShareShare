from django import forms
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import User, UserManager

from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.ModelForm):
    userMail = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Email address'),
                'required': 'True',
            }
        )
    )
    nickname = forms.CharField(
        label=_('Nickname'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Nickname'),
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('userMail', 'nickname')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['userMail'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ShareeSignupForm(SignupForm):
    location = forms.CharField(
        label=_('Location'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Location'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('userMail', 'nickname', 'location')

    def save(self, commit=True):
        user = super(ShareeSignupForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['userMail'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SharerSignupForm(SignupForm):
    class Meta:
        model = User
        fields = ('userMail', 'nickname')

    def save(self, commit=True):
        user = super(SharerSignupForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['userMail'])
        user.is_sharer = True
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['username', 'password']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('userMail', 'password', 'is_active', 'is_superuser')
