from django.forms import ModelForm
from .models import User
from django import forms
from django.contrib.auth.hashers import make_password


class CreateUserForm(ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    # confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    # email = forms.EmailField(max_length=255)
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,9}$', max_length=9
    )

    zip_code = forms.RegexField(
        regex=r"^\d{2}(?:[-\s]\d{3})$", max_length=6
    )

    class Meta:
        model = User
        fields = ["name", "surname", "phone_number", "zip_code", "phone_number"]

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Password does not match")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]
