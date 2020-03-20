from django.db import models
from asgiref.sync import sync_to_async


class BaseKurs(models.Model):
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2)
    harga_beli = models.DecimalField(max_digits=12, decimal_places=2)
    tanggal_dan_waktu = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Dinar(BaseKurs):

    def __str__(self):
        return f'Dinar: {self.harga_jual}'


class Dirham(BaseKurs):

    def __str__(self):
        return f'Dirham: {self.harga_jual}'


dinar_get_all = sync_to_async(Dinar.objects.all)
dinar_create = sync_to_async(Dinar.objects.create)

dirham_get_all = sync_to_async(Dirham.objects.all)
dirham_create = sync_to_async(Dirham.objects.create)