from decimal import Decimal
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# from somewhere import handle_uploaded_file 

from .models import *
from .forms import *
from django.db.models import F, Q

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    else: 
        return render(request, "index.html")

def login(request):
    if request.method == 'POST':
        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
            # return render('dashboard')
            # return HttpResponse('Authenticated successfully')
                
        else:
            # return HttpResponse('Authenticated disabled')
            # print(username,password)
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password.',
                'title': 'Login',
            })
    else:
        return render(request, 'login.html', {
            'title': 'Login',
        })

@login_required
def dashboard(request):
    
    currentYear= timezone.now().year
    currentDay= timezone.now().day
    return render(request, "dashboardAdmin.html",{
        'bengkel_count': Bengkel.objects.count(),
        'supplier_count': Supplier.objects.count(),
        'product_count': Product.objects.count(),
        'need_stock': Stock.objects.filter(stockCount__lt=F('minStock')).count(),
        # 'transaksi_sebulan': Order.objects.filter(orderDate__year=currentYear, orderDate__month=11).count(),
        'transaksi_setahun': Order.objects.filter(orderDate__year=currentYear).count(),
        'penawaran_today': Penawaran.objects.filter(tawarDate__day=currentDay).count(),
        'produk_tambahan_today': Product.objects.filter(addDate__day=currentDay).count(),
    })
    # return HttpResponse(request.user.role)

@login_required
def bengkel(request):
    return render(request, "bengkel.html",{
        'bengkel': Bengkel.objects.select_related("owner").all(),
    })

@login_required
def bengkelDetail(request, bengkel_id):
    bengkel = Bengkel.objects.select_related("owner").get(id=bengkel_id)
    return render(request, "bengkelDetail.html",{
        'bengkel': bengkel,
        # 'stock': Stock.objects.select_related("product").filter(bengkel=bengkel_id),
        'stock': Stock.objects.prefetch_related("product__brand","product__category","product__supplier").filter(bengkel=bengkel_id),
    })

@login_required
def editBengkel(request, bengkel_id, stock_id):
    return render(request, "editStock.html",{
        'stock': Stock.objects.prefetch_related("product__brand","product__category","product__supplier").get(id=stock_id),
    })

@login_required
def saveStock(request, stock_id):
    stock = Stock.objects.select_related("bengkel").get(id=stock_id)
    minStock = int(request.POST['minStock'])
    stock.minStock = minStock
    stock.save()
    
    return HttpResponseRedirect('/bengkel/'+str(stock.bengkel.id),{
        'message': "Data Berhasil disimpan", #ga bisa njir
    })

@login_required
def supplier(request):
    return render(request, "supplier.html",{
        'supplier': Supplier.objects.select_related("owner").all(),
        # 'tes': Supplier.objects.values(),
    })

@login_required
def supplierDetail(request, supplier_id):
    supplier = Supplier.objects.select_related("owner").get(id=supplier_id)
    return render(request, "supplierDetail.html",{
        'supplier': supplier,
        # 'stock': Stock.objects.select_related("product").filter(bengkel=bengkel_id),
        'product': Product.objects.prefetch_related("category","brand").filter(supplier=supplier_id),
    })


@login_required
def transaksi(request):
    return render(request, "transaksi.html",{
        'transaksi': Order.objects.select_related("supplier").all(),
        # 'tes': Supplier.objects.values(),

    })

@login_required
def transaksiDetail(request, order_id):
    
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = TransaksiForm(request.POST, request.FILES)
        form.instance.id = order.id
        form.instance.supplier = order.supplier
        form.instance.bengkel = order.bengkel
        form.instance.orderDate = order.orderDate
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/transaksi/')
            # return HttpResponseRedirect('/transaksi/'+str(order_id))
    else:
          form =  TransaksiForm
    return render(request, 'transaksiDetail.html',{
                'order': order,
                'form':form,
                'transaksi': OrderItem.objects.prefetch_related("orderId","product", "product__brand","product__category",).filter(orderId_id=order_id),
            })
    
# class TransaksiCreate(LoginRequiredMixin, CreateView):
#     model = Order
#     template_name = "transaksiCreate.html"
#     form_class = TransaksiBaru, OrderItemForm


#     def form_valid(self, form):
#         form.instance.penawar = (self.request.user)
#         return super().form_valid(form)

@login_required
def transaksiCreate(request):
    return HttpResponse('a')


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))

# @login_required
# class createTransaksi()

@login_required
def penawaran(request, account):
    return render(request, "penawaran.html",{
        'penawaran': Penawaran.objects.filter(Q(tujuan_id=account) | Q(penawar_id=account)),
    })


class PenawaranCreate(LoginRequiredMixin, CreateView):
    model = Penawaran
    template_name = "penawaranCreate.html"
    form_class = PenawaranForm


    def form_valid(self, form):
        form.instance.penawar = (self.request.user)
        return super().form_valid(form)


@login_required
def editAccount(request, account_name):
    return render(request, "profile.html",{})

@login_required
def saveAccount(request, account_name):
    account = Account.objects.get(username=account_name)
    account.username = (request.POST['username'])
    account.set_password(request.POST['password'])
    account.name = (request.POST['name'])
    account.address = (request.POST['address'])
    account.phone = (request.POST['phone'])
    account.telegram = (request.POST['telegram'])
    account.save()
    
    return HttpResponseRedirect('/dashboard/',{
        'message': "Data Berhasil disimpan", #ga bisa njir
    })
