"""Creation of the user account form."""


# Django imports
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User



class AccountForm(ModelForm):
    """Form to create the user register account, based on the Django User model."""

    class Meta:
        """Details of the register form and attributes settings for CSS."""
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'username', 'placeholder': 'Entrez votre nom d\'utilisateur'}),
            'email': EmailInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'inputEmail', 'placeholder': 'Entrez votre email', 'required': 'required'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'inputPassword', 'placeholder': 'Entrez votre mot de passe'})
        }
