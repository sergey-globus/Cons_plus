from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['first_name', 'last_name', 'phone', 'question']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите ваш вопрос'})
        }

class DocumentGeneratorForm(forms.Form):
    template_id = forms.IntegerField(widget=forms.HiddenInput())
    first_name = forms.CharField(max_length=50, label="Имя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(max_length=50, label="Отчество", widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_number = forms.CharField(max_length=20, label="Номер паспорта", widget=forms.TextInput(attrs={'class': 'form-control'}))
    contract_number = forms.CharField(max_length=50, label="Номер договора", widget=forms.TextInput(attrs={'class': 'form-control'}))
