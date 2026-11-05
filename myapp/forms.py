from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import DriverProfile, Order, Product, Profile, Review


class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    phone = forms.CharField(max_length=30)
    county = forms.CharField(max_length=80)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "role", "phone", "county")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "category", "description", "county", "price_per_kg", "quantity_kg", "minimum_order_kg", "available_from", "image_url", "organic")
        widgets = {"available_from": forms.DateInput(attrs={"type": "date"})}


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("quantity_kg", "driver")

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product:
            self.fields["driver"].queryset = DriverProfile.objects.filter(available=True, capacity_kg__gte=product.minimum_order_kg)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
