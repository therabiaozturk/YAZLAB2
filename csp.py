from datetime import datetime

def agirlik_kontrol(drone, teslimat):
    return teslimat.weight <= drone.max_weight

def zaman_kontrol(teslimat, mevcut_saat):
    baslangic, bitis = teslimat.time_window
    fmt = "%H:%M"
    bas = datetime.strptime(baslangic, fmt)
    bit = datetime.strptime(bitis, fmt)
    simdi = datetime.strptime(mevcut_saat, fmt)
    return bas <= simdi <= bit

def nokta_noflyzone_icinde_mi(pos, noflyzones, saat):
    x, y = pos
    for zone in noflyzones:
        bas, bit = zone.active_time
        if saat < bas or saat > bit:
            continue  # aktif değilse geç
        xs = [c[0] for c in zone.coordinates]
        ys = [c[1] for c in zone.coordinates]
        if min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys):
            return True
    return False

def teslimat_mumkun_mu(drone, teslimat, noflyzones, saat):
    if not agirlik_kontrol(drone, teslimat):
        return False
    if not zaman_kontrol(teslimat, saat):
        return False
    if nokta_noflyzone_icinde_mi(teslimat.pos, noflyzones, saat):
        return False
    return True
