from django import forms
from .models import Order, OrderItem, Supplier, Bengkel, Product, Stock, Brand, Category, Penawaran
# , OrderItem, Supplier, Bengkel, Product, Stock, Brand, Category

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['bukti']


class PenawaranForm(forms.ModelForm):
    class Meta:
        model = Penawaran
        fields = ['tujuan','deskripsi']
        widgets = {
            'deskripsi': forms.Textarea(attrs={'class': 'form-control'}),
            'tujuan': forms.Select(attrs={'class': 'form-control'}),
        }

class TransaksiBaru(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supplier','bengkel']

class OrderItemForm(forms.ModelForm):
    
    class Meta:
        model = OrderItem
        fields = ['quantity','product']
