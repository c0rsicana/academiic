from decimal import Decimal

from academiic_apps.management.models import Level, Section, AcademicYear
from academiic_apps.student.models import Students
from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.


class Invoice(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    books = models.DecimalField(max_digits=10, decimal_places=2)
    tuition = models.DecimalField(max_digits=10, decimal_places=2)
    academic_Year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["student"]

    def __str__(self):
        return f"{self.student}"

    def amount_payable(self):
        books = self.books
        tuition = self.tuition
        total = books + tuition
        return total

    def amount_paid(self):
        receipts = Receipt.objects.filter(invoice=self)
        amount = 0
        for receipts in receipts:
            amount += receipts.amount_paid
        return amount

    def balance(self):
        payable = self.amount_payable()
        paid = self.amount_paid()
        return payable - paid

    def get_absolute_url(self):
        return reverse("view_invoice", kwargs={"pk": self.pk})

class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    date_paid = models.DateField(null=True)
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Receipt on {self.date_paid}"
