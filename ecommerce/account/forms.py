from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import Customer, Address


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line',
                  'address_line2', 'town_city', 'postcode']
        #exclude = ['id', 'customer', 'delivery_instructions', 'created_at', 'updated_at', ' default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"placeholder": "Полное имя"}
        )
        self.fields["phone"].widget.attrs.update(
            { "placeholder": "Номер телефона"})
        self.fields["address_line"].widget.attrs.update(
            {"placeholder": "Адрес"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"placeholder": "Дополнительный адрес"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"placeholder": "Населенный пункт"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"placeholder": "Почтовый индекс"}
        )


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Введите имя', max_length=50, help_text='* обязательное поле')
    email = forms.EmailField(max_length=100, help_text='* обязательное поле',
                             error_messages={'обязательно': 'Вы не предоставили email'})
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('user_name', 'email')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError(
                'Пользователь с таким именем уже существует')
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Данный email занят. Пожалуйста, используйте другой')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Введите email', 'id': 'login-username'}))
    password: forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
        'id': 'login-pwd', }))


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'id': 'form-email', }))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError('Email не найден')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1: forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'новый пароль', 'id': 'form-newpass'
    }))
    new_password2: forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'повторите пароль', 'id': 'form-newpass2'
    }))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Электронная почта аккаунта (не может быть изменена)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Имя', max_length=50, widget=forms.TextInput(
            attrs={'placeholder': 'введите имя', 'id': 'form-firstname',}))

    mobile = forms.CharField(
        label='номер телефона', max_length=50, widget=forms.TextInput(
            attrs={'placeholder': 'введите номер телефона', 'id': 'form-lastname'}))

    class Meta:
        model = Customer
        fields = ('email', 'user_name', 'mobile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['user_name'].required = True