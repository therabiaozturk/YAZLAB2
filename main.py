from veri_uretimi import drone_uret, teslimat_uret, noflyzone_uret
from algoritma import astar
from genetik import genetik_algoritma
from gorsel import rota_ciz
from datetime import datetime

import time
from veri_uretimi import drone_uret, teslimat_uret, noflyzone_uret
from genetik import genetik_algoritma
from csp import teslimat_mumkun_mu, agirlik_kontrol

# 1. Veri üretimi
dronelar = drone_uret(1)  # tek drone ile başlıyoruz
teslimatlar = teslimat_uret(5)
noflyzones = noflyzone_uret(2)
saat = "09:30"

# 2. Drone seç
drone = dronelar[0]
print(f"\nKullanılan Drone: {drone}")

# 3. Genetik Algoritma ile rota bul
print("\nGenetik algoritma ile rota bulunuyor...")
rota = genetik_algoritma(drone, teslimatlar, noflyzones, saat)
print("\nEn iyi rota:")
for t in rota:
    print(f"  -> Teslimat#{t.id} @ {t.pos}")

# 4. Görselleştir
rota_ciz(drone, rota, noflyzones)
"""
def test_senaryosu(drone_sayisi, teslimat_sayisi, nofly_sayisi):
    saat = "09:30"
    dronelar = drone_uret(drone_sayisi)
    teslimatlar = teslimat_uret(teslimat_sayisi)
    noflyzones = noflyzone_uret(nofly_sayisi)

    baslangic_zamani = time.time()
    toplam_teslimat = 0
    toplam_enerji = 0

    for drone in dronelar:
        rota = genetik_algoritma(drone, teslimatlar, noflyzones, saat)
        enerji = sum(t.weight * 5 for t in rota)
        basarili = sum(1 for t in rota if teslimat_mumkun_mu(drone, t, noflyzones, saat))
        toplam_teslimat += basarili
        toplam_enerji += enerji

    bitis_zamani = time.time()
    calisma_suresi = round(bitis_zamani - baslangic_zamani, 2)
    ort_enerji = round(toplam_enerji / drone_sayisi, 2)

    print(f"\n Test Sonuçları (D:{drone_sayisi} T:{teslimat_sayisi} N:{nofly_sayisi})")
    print(f" Toplam Teslimat: {toplam_teslimat}")
    print(f" Ortalama Enerji: {ort_enerji} birim")
    print(f" Süre: {calisma_suresi} saniye")

test_senaryosu(5, 20, 2)  # Senaryo 1
test_senaryosu(10, 50, 5) # Senaryo 2 """
def astar_senaryosu(drone_sayisi, teslimat_sayisi, nofly_sayisi):
    saat = "09:30"
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
                toplam_enerji += hedef.weight * 5  # basit enerji modeli
                drone.start_pos = hedef.pos  # drone yeni konuma gider
                ziyaret_edilen.append(hedef)

    bitis = time.time()
    ort_enerji = round(toplam_enerji / drone_sayisi, 2) if drone_sayisi > 0 else 0
    calisma_suresi = round(bitis - baslangic, 2)
    print(f"\n📊 A* Test Sonuçları (D:{drone_sayisi} T:{teslimat_sayisi} N:{nofly_sayisi})")
    print(f"✔️ Toplam Teslimat: {toplam_teslimat}")
    print(f"⚡ Ortalama Enerji: {ort_enerji} birim")
    print(f"⏱️ Süre: {calisma_suresi} saniye")

astar_senaryosu(5, 20, 2)   # Senaryo 1
astar_senaryosu(10, 50, 5)  # Senaryo 2
