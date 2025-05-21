from veri_uretimi import drone_uret, teslimat_uret, noflyzone_uret
from algoritma import astar
from genetik import genetik_algoritma
from gorsel import rota_ciz
from datetime import datetime

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
