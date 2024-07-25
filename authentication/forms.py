from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'firstname', 'othernames', 'role')

        widgets = {
            "email": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "firstname": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "othernames": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "role": forms.EmailInput(attrs={
                "class": "form-control",
            })
        }


class CustomUserUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'firstname', 'othernames', 'role', 'phone_number', 'pass_port_photo')


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'password_too_similar': _('Your password can’t be too similar to your other personal information.'),
        'password_too_short': _('Your password must contain at least 8 characters.'),
        'password_common': _('Your password can’t be a commonly used password.'),
        'password_entirely_numeric': _('Your password can’t be entirely numeric.'),
        'password_incorrect': _('Your old password was entered incorrectly. Please enter it again.'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        user = self.user

        if password1:
            if user.check_password(password1):
                raise forms.ValidationError(
                    _("Your new password must be different from the old password."),
                    code='password_no_change',
                )

            if password1 == user.get_username():
                raise forms.ValidationError(
                    self.error_messages['password_too_similar'],
                    code='password_too_similar',
                )

            if len(password1) < 8:
                raise forms.ValidationError(
                    self.error_messages['password_too_short'],
                    code='password_too_short',
                )

            if password1.isnumeric():
                raise forms.ValidationError(
                    self.error_messages['password_entirely_numeric'],
                    code='password_entirely_numeric',
                )

            common_passwords = [
                'password', '12345678', '123456789', '123456', '1234567',
                '12345', '1234567890', 'qwerty', 'abc123', 'password1'
            ]
            if password1.lower() in common_passwords:
                raise forms.ValidationError(
                    self.error_messages['password_common'],
                    code='password_common',
                )

        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2