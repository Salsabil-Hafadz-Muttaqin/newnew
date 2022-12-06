
from django.contrib.auth.models import AbstractUser

# from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.db import models



class Account(AbstractUser):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Role_type(models.TextChoices):
        admin = "AD", ("Super Admin")
        supervisor = "SV", ("Supervisor")
        lead_bengkel = "LB", ("Pimpinan Bengkel")
        supplier = "SP", ("Supplier")

    # username = models.CharField(blank=False, max_length=25, unique=True)
    name = models.CharField(blank=False, max_length=50)
    # password = models.CharField(max_length=16)
    telegram = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    role = models.CharField(choices=Role_type.choices, max_length=40)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("Account_detail", kwargs={"pk": self.pk})


class Supplier(models.Model):
    name = models.CharField(blank=False, max_length=50)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Suppliers"
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("Supplier_detail", kwargs={"pk": self.pk})


class Bengkel(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Bengkel-Bengkel"
        ordering = ['name']

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Bengkel_detail", kwargs={"pk": self.pk})


class Brand(models.Model):
    name = models.CharField(blank=False, max_length=50)

    class Meta:
        verbose_name_plural = "Brands"
        ordering = ['name']

    def __str__(self):
        # return f"Brand {self.name}"
        return str(self.name)

    def get_absolute_url(self):
        return reverse("Brand_detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(blank=False, max_length=50)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    name = models.CharField(blank=False, max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="media/", height_field=None, width_field=None, max_length=None
    )
    category = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    addDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    updateDate = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bengkel = models.ForeignKey(Bengkel, on_delete=models.CASCADE)
    stockCount = models.PositiveIntegerField()
    minStock = models.PositiveIntegerField()

    def __str__(self):
        return str(self.product) + " " + str(self.bengkel)

    class Meta:
        ordering = ["-stockCount"]


class Order(models.Model):

    orderDate = models.DateTimeField(auto_now_add=True)
    isApprove = models.BooleanField(default=False)
    bukti = models.ImageField(upload_to="media/")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    bengkel = models.ForeignKey(Bengkel, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.orderDate)

    def get_absolute_url(self):
        return reverse("dashboard")
    
    class Meta:
        ordering = ['-orderDate','isApprove']


class OrderItem(models.Model):
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.orderId)

    # def get_absolute_url(self):
    #     return reverse("OrderItem_detail", kwargs={"pk": self.pk})

class Penawaran(models.Model):
    tawarDate = models.DateTimeField(auto_now_add=True)
    penawar = models.ForeignKey(Account, related_name='penawar', on_delete=models.CASCADE)
    tujuan = models.ForeignKey(Account, related_name="tujuan" , on_delete=models.CASCADE)
    deskripsi = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = ("Penawaran-Penawaran")
        ordering = ['-tawarDate']

    def __str__(self):
        return str(self.tawarDate)

    def get_absolute_url(self):
        return reverse("dashboard")

