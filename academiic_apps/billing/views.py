from academiic_apps.billing.forms import Billing, \
    ReceiptForm_test, ReceiptFormSet
from academiic_apps.billing.models import Invoice, Receipt
from academiic_apps.management.models import AcademicYear
from academiic_apps.student.models import Students
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
# Create your views here.


class CreateInvoicesView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = "Invoice.create_invoice"
    permission_denied_message = "You do not have access to this page"
    template_name = 'billing/create_invoice.html'
    form_class = Billing
    success_message = "Invoice Created"
    success_url = reverse_lazy('list_invoice')

    def form_valid(self, form):
        year_level = form.cleaned_data['year_level'].id
        students = Students.objects.filter(level=year_level)
        academic_Year = AcademicYear.objects.get(active=True)
        tuition = form.cleaned_data['tuition']
        books = form.cleaned_data['books']

        for student in students:
            Invoice.objects.create(student=student, tuition=tuition, books=books, academic_Year=academic_Year)

        return super().form_valid(form)


class ListInvoicesView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "billing/list_invoice.html"


class InvoiceView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = "billing/invoice.html"

    def get_context_data(self, **kwargs):
        context = super(InvoiceView, self).get_context_data(**kwargs)
        context["receipts"] = Receipt.objects.filter(invoice=self.object)
        return context


class UpdateInvoiceView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Invoice.change_invoice"
    permission_denied_message = 'You do not have access to this page'
    template_name = 'billing/update_invoice.html'
    model = Invoice
    success_message = "Invoice Updated Successfully!"
    fields = [
        "tuition",
        "books"
    ]

    def get_context_data(self, **kwargs):
        context = super(UpdateInvoiceView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["receipts"] = ReceiptFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["receipts"] = ReceiptFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["receipts"]
        if form.is_valid() and formset.is_valid:
            form.save()
            formset.save()
        return super().form_valid(form)


class CreateReceiptView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "billing/create_receipt.html"
    permission_required = "Receipt.add_receipt"
    permission_denied_message = 'You do not have access to this page'
    form_class = ReceiptForm_test
    model = Receipt
    success_url = reverse_lazy("list_invoice")
    success_message = "Receipt added successfully!"

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        obj.invoice = invoice
        obj.save()
        return redirect("list_invoice")

    def get_context_data(self, **kwargs):
        context = super(CreateReceiptView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        context["invoice"] = invoice
        return context


class DeleteInvoiceView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "Invoice.delete_invoice"
    permission_denied_message = 'You do not have access to this page'
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_message = "Invoice Deleted"
    success_url = reverse_lazy("list_invoice")

