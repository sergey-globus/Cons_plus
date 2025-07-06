from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['middle_name', 'passport_number', 'age', 'phone']
        widgets = {
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 567890'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '100'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
        }
