from veri_uretimi import drone_uret, teslimat_uret, noflyzone_uret, sabit_dron_nesneleri, sabit_teslimat_nesneleri, sabit_noflyzone_nesneleri
from algoritma import astar
from genetik import genetik_algoritma
from gorsel import rota_ciz
from datetime import datetime

import time
from csp import teslimat_mumkun_mu, agirlik_kontrol

# 1. Veri üretimi
veri_turu = "Rastgele"  # Arayüzden alınacak şekilde ayarlandı

def calistir(drone_sayisi, teslimat_sayisi, nofly_sayisi, veri_turu_input):
    saat = "09:30"
    global veri_turu
    veri_turu = veri_turu_input

    if veri_turu == "Sabit":
        dronelar = sabit_dron_nesneleri()
        teslimatlar = sabit_teslimat_nesneleri()
        noflyzones = sabit_noflyzone_nesneleri()
    else:
        dronelar = drone_uret(drone_sayisi)
        teslimatlar = teslimat_uret(teslimat_sayisi)
        noflyzones = noflyzone_uret(nofly_sayisi)

    drone = dronelar[0]
    print(f"\nKullanılan Drone: {drone}")

    print("\nGenetik algoritma ile rota bulunuyor...")
    rota = genetik_algoritma(drone, teslimatlar, noflyzones, saat)
    print("\nEn iyi rota:")
    for t in rota:
        print(f"  -> Teslimat#{t.id} @ {t.pos}")

    rota_ciz(drone, rota, noflyzones)

def astar_senaryosu(drone_sayisi, teslimat_sayisi, nofly_sayisi):
    saat = "09:30"

    if veri_turu == "Sabit":
        dronelar = sabit_dron_nesneleri()
        teslimatlar = sabit_teslimat_nesneleri()
        noflyzones = sabit_noflyzone_nesneleri()
    else:
        dronelar = drone_uret(drone_sayisi)
        teslimatlar = teslimat_uret(teslimat_sayisi)
        noflyzones = noflyzone_uret(nofly_sayisi)

    baslangic = time.time()
    toplam_teslimat = 0
    toplam_enerji = 0

    for drone in dronelar:
        uygun_teslimatlar = [t for t in teslimatlar if teslimat_mumkun_mu(drone, t, noflyzones, saat)]
        ziyaret_edilen = []

        while uygun_teslimatlar:
            hedef = uygun_teslimatlar.pop(0)
            rota = astar(drone, hedef.pos, noflyzones)
            if rota:
                toplam_teslimat += 1
                toplam_enerji += hedef.weight * 5
                drone.start_pos = hedef.pos
                ziyaret_edilen.append(hedef)

    bitis = time.time()
    ort_enerji = round(toplam_enerji / drone_sayisi, 2) if drone_sayisi > 0 else 0
    calisma_suresi = round(bitis - baslangic, 2)
    print(f"\n📊 A* Test Sonuçları (D:{drone_sayisi} T:{teslimat_sayisi} N:{nofly_sayisi})")
    print(f"✔️ Toplam Teslimat: {toplam_teslimat}")
    print(f"⚡ Ortalama Enerji: {ort_enerji} birim")
    print(f"⏱️ Süre: {calisma_suresi} saniye")

# Örnek çağrılar
# calistir(1, 5, 2, "Rastgele")
# astar_senaryosu(5, 20, 2)
