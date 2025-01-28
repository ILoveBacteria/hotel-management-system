from django.forms import ModelForm

from payments.models import Bill, CreditCard


class CardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ['number', 'expire_month', 'cvv2', 'expire_year', 'password']