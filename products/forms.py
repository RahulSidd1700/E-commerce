from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1,
    widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'}))