from django.urls import path
from . import views
from management.views import PenawaranCreate
# from management.views import PenawaranCreate, TransaksiCreate

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("bengkel/", views.bengkel, name="bengkel"),
    path("supplier/", views.supplier, name="supplier"),
    path("transaksi/", views.transaksi, name='transaksi'),
    path("bengkel/<str:bengkel_id>/", views.bengkelDetail, name="bengkelDetail"),
    path("bengkel/<str:bengkel_id>/edit/<str:stock_id>/", views.editBengkel, name="editBengkel"),
    path("bengkel/stock/<str:stock_id>/save", views.saveStock, name="saveStock"),
    path("supplier/<str:supplier_id>", views.supplierDetail, name="supplierDetail"),
    path("transaksi/<str:order_id>", views.transaksiDetail, name="transaksiDetail"),
    path("transaksi/create/", views.transaksiCreate, name="transaksiCreate"),
    # path("transaksi/create/", TransaksiCreate.as_view(), name="transaksiCreate"),
    path("penawaran/<str:account>/", views.penawaran, name="penawaran"),
    path("penawaran/<str:account>/create", PenawaranCreate.as_view(), name="penawaranCreate"),
    path("account/<str:account_name>",views.editAccount, name="editAccount"),
    path("account/<str:account_name>/save",views.saveAccount, name="saveAccount"),
]
