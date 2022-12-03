from django.forms import ModelForm
from .models import OrderData, User, Wine
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
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nazwa wina"}))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Opis",
                "rows": 5,
                "cols": 23,
                "style": "resize: none",
            }
        ),
    )
    price = forms.DecimalField(
        widget=forms.TextInput(attrs={"placeholder": "Cena"}),
    )
    producer = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Producent"})
    )
    color = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Color"}))
    flavor = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Smak"}))
    strain = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Szczep"}))
    aroma = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Aromat"}))
    vol = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "Alkohol [%]"}))
    size = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "Objętość [ml]"}))
    in_stock = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "Ilość produktu na magazynie"}))

    error_messages = {
        'in_stock': {
            'validators': ("This writer's name is too long."),
        },
    }

    class Meta:
        model = Wine
        fields = [
            "name",
            "description",
            "price",
            "producer",
            "image",
            "color",
            "flavor",
            "strain",
            "aroma",
            "vol",
            "size",
            "in_stock",
        ]


class RatingForm(ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Twoja opinia",
                "style": "resize: none",
            }
        ),
    )

    class Meta:
        model = Wine
        fields = [
            "description"
        ]


class SubmitOrderForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Jan"}))
    surname = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Kowalski"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "przyklad@email.com"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Miasto"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "999999999"}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "99-999"}))
    address_and_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Ulica 1"}))

    class Meta:
        model = OrderData
        fields = [
            "name",
            "surname",
            "email",
            "city",
            "phone_number",
            "zip_code",
            "address_and_number",
        ]
