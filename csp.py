from datetime import datetime

# ➕ Yeni: Şarj kontrolü
def sarj_kontrol(drone, teslimat):
    enerji_ihtiyaci = teslimat.weight * 5  # Basit enerji modeli
    return drone.battery >= enerji_ihtiyaci

# ➕ Ağırlık kontrolü
def agirlik_kontrol(drone, teslimat):
    return teslimat.weight <= drone.max_weight

# ➕ Zaman kontrolü
def zaman_kontrol(teslimat, mevcut_saat):
    baslangic, bitis = teslimat.time_window
    fmt = "%H:%M"
    bas = datetime.strptime(baslangic, fmt)
    bit = datetime.strptime(bitis, fmt)
    simdi = datetime.strptime(mevcut_saat, fmt)
    return bas <= simdi <= bit

# ➕ No-fly zone kontrolü
def nokta_noflyzone_icinde_mi(pos, noflyzones, saat):
    x, y = pos
    for zone in noflyzones:
        bas, bit = zone.active_time
        if saat < bas or saat > bit:
            continue
        xs = [c[0] for c in zone.coordinates]
        ys = [c[1] for c in zone.coordinates]
        if min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys):
            return True
    return False

# 🔄 Ana kontrol: Tüm kuralları birleştirir
def teslimat_mumkun_mu(drone, teslimat, noflyzones, saat):
    return (
        agirlik_kontrol(drone, teslimat)
        and zaman_kontrol(teslimat, saat)
        and not nokta_noflyzone_icinde_mi(teslimat.pos, noflyzones, saat)
        and sarj_kontrol(drone, teslimat)  # 🔋 Şarj kontrolü eklendi
    )
