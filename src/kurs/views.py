import asyncio
from asgiref.sync import sync_to_async
from django.shortcuts import render, redirect
from .scrapper import get_latest_kurs
from .models import (dirham_create, dinar_create, dirham_get_all, dinar_get_all,
                     Dinar, Dirham)


async def index_view(request):
    list_dinar, list_dirham = await asyncio.gather(
        dinar_get_all(),
        dirham_get_all()
    )
    context = {
        'list_dinar': list_dinar,
        'list_dirham': list_dirham,
    }
    return await sync_to_async(render)(request, 'index.html', context)


async def fetch_view(request):
    kurs = await get_latest_kurs()
    await asyncio.gather(
        dinar_create(**{
            'harga_jual': kurs['dinar']['jual'],
            'harga_beli': kurs['dinar']['beli']
        }),
        dirham_create(**{
            'harga_jual': kurs['dirham']['jual'],
            'harga_beli': kurs['dirham']['beli']
        })
    )
    return redirect('index')


async def remove_view(request):
    await asyncio.gather(
        sync_to_async(Dinar.objects.all().delete)(),
        sync_to_async(Dirham.objects.all().delete)(),
    )
    return redirect('index')

