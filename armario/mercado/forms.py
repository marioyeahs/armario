from django import forms

class PurchaseForm(forms.Form):
    price = forms.IntegerField()
    size = forms.CharField(max_length=5)
    total = forms.FloatField()

class RegisterForm(forms.Form):
    usuario = forms.CharField(max_length=250)
    phone = forms.IntegerField()
    email = forms.EmailField(label='E-mail')
    passwd = forms.CharField(max_length=250, widget=forms.PasswordInput)

    def send_email(self):
        email = self.cleaned_data['email']
        print(f"email enviado {email}")

