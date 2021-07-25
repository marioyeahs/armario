from django import forms

class sizeForm(forms.Form):
    monto = forms.IntegerField()

class registerForm(forms.Form):
    usuario = forms.CharField(max_length=250)
    phone = forms.IntegerField()
    email = forms.EmailField(label='E-mail')
    passwd = forms.CharField(max_length=250, widget=forms.PasswordInput)