from django.urls import path
from .views import CreateInvoicesView, ListInvoicesView, CreateReceiptView, \
    InvoiceView, UpdateInvoiceView, DeleteInvoiceView

urlpatterns = [
    path('create_invoice', CreateInvoicesView.as_view(), name='create_invoice'),
    path('list_invoice', ListInvoicesView.as_view(), name='list_invoice'),
    path('invoice_detail/<int:pk>', InvoiceView.as_view(), name='view_invoice'),
    path('update_invoice/<int:pk>', UpdateInvoiceView.as_view(), name='update_invoice'),
    path('delete_invoice/<int:pk>', DeleteInvoiceView.as_view(), name='delete_invoice'),
    path('create_receipt', CreateReceiptView.as_view(), name='create_receipt'),
]