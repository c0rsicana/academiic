from academiic_apps.billing.models import Receipt, Invoice
from academiic_apps.management.models import Level
from academiic_apps.student.models import Students
from django import forms
from django.forms import inlineformset_factory, TextInput


class DateInput(forms.DateInput):
    input_type = 'date'


class Billing(forms.Form):
    year_level = forms.ModelChoiceField(queryset=Level.objects.all(), empty_label="Select Year Level")
    tuition = forms.DecimalField(max_digits=10, decimal_places=2)
    books = forms.DecimalField(max_digits=10, decimal_places=2)
    academic_Year = forms.HiddenInput()


class ReceiptForm_test(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = [
            "amount_paid",
            "date_paid",
            "comment",
        ]
        widgets = {
            "date_paid": DateInput()
        }


ReceiptFormSet = inlineformset_factory(
    Invoice, Receipt, fields=("amount_paid", "date_paid", "comment"), widgets={"date_paid": DateInput}, extra=0, can_delete=True
)

