from django import forms
from .models import Consultation
from .crypto import GOSTCrypto

crypto = GOSTCrypto()
from django import forms
from .models import Consultation

class ConsultationForm(forms.Form):
    first_name = forms.CharField(
        label='Имя',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    question = forms.CharField(
        label='Вопрос',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    
    def save(self):
        consultation = Consultation()
        consultation.first_name = self.cleaned_data['first_name']
        consultation.last_name = self.cleaned_data['last_name']
        consultation.email = self.cleaned_data['email']
        consultation.question = self.cleaned_data['question']
        consultation.save()
        return consultation

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
    def clean(self):
        cleaned_data = super().clean()
        sensitive_fields = ['first_name', 'last_name', 'middle_name', 
                           'passport_number', 'phone', 'email', 'address']
        
        for field in sensitive_fields:
            if field in cleaned_data and cleaned_data[field]:
                cleaned_data[field] = crypto.encrypt(cleaned_data[field])
        
        return cleaned_data
