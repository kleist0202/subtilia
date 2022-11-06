from django.forms import ModelForm
from .models import User, Wine
from django import forms
from django.contrib.auth.hashers import make_password


class CreateUserForm(ModelForm):
    email = forms.EmailField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Adres email"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}), min_length=8
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}), min_length=8
    )
    # name = forms.CharField(max_length=50)
    # surname = forms.CharField(max_length=50)
    # phone_number = forms.RegexField(
    #     regex=r'^\+?1?\d{9,9}$', max_length=9
    # )
    #
    # zip_code = forms.RegexField(
    #     regex=r"^\d{2}(?:[-\s]\d{3})$", max_length=6
    # )

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]

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


class AddWineForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Nazwa wina"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Opis", "rows":5, "cols":23, "style": "resize: none"}),
    )
    price = forms.DecimalField(
        widget=forms.TextInput(attrs={"placeholder": "Cena"}),
    )

    class Meta:
        model = Wine
        fields = ["name", "description", "price", "image"]
