from django import forms
from .models import Consultation

# forms.py
from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['first_name', 'last_name', 'email', 'question']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вашу фамилию'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com'
            }),
            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Опишите вашу ситуацию подробно...'
            }),
        }

class DocumentGeneratorForm(forms.Form):
    template_id = forms.IntegerField(widget=forms.HiddenInput())
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    middle_name = forms.CharField(max_length=50, required=False)
    passport_number = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    date = forms.DateField(required=False)
    order_number = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=200, required=False)
    seller_name = forms.CharField(max_length=200, required=False)
    product_name = forms.CharField(max_length=200, required=False)
    product_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    product_article = forms.CharField(max_length=100, required=False)
    purchase_date = forms.DateField(required=False)
    order_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    date_order = forms.DateField(required=False)
    return_reason = forms.CharField(max_length=200, required=False)
    violation_description = forms.CharField(widget=forms.Textarea, required=False)
    demands = forms.CharField(widget=forms.Textarea, required=False)
