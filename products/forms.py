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
    
    
class ShippingAddressForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address_line_1 = forms.CharField(label='Address Line 1', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address_line_2 = forms.CharField(label='Address Line 2', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label='City', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(label='State/Province', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(label='ZIP/Postal Code', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='Country', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

class PaymentMethodForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cod', 'Cash on Delivery'),
    ]
    payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))