import tkinter as tk
from tkinter import messagebox
from veri_uretimi import drone_uret, teslimat_uret, noflyzone_uret, NoFlyZone
from genetik import genetik_algoritma
from algoritma import astar, astar_static_graph
from csp import teslimat_mumkun_mu
from gorsel import rota_ciz
from utils import mesafe_hesapla
from shapely.geometry import LineString, Polygon
import time


def cizgi_nofly_icinden_geciyor_mu(a, b, noflyzones, simdi_saat):
    cizgi = LineString([a, b])
    for zone in noflyzones:
        if hasattr(zone, "aktif_mi") and not zone.aktif_mi(simdi_saat):
            continue
        rect = Polygon(zone.coordinates)
        if cizgi.intersects(rect):
            return True
    return False


def baslat():
    try:
        drone_sayisi = int(entry_drone.get())
        teslimat_sayisi = int(entry_teslimat.get())
        nofly_sayisi = int(entry_nofly.get())
        algoritma = secili_algoritma.get()
        saat = entry_saat.get() or "09:30"

        dronelar = drone_uret(drone_sayisi)
        teslimatlar = teslimat_uret(teslimat_sayisi)
        noflyzones = noflyzone_uret(nofly_sayisi)

        drone = dronelar[0]
        baslangic = time.time()
        ceza_adedi = 0
        toplam_bekleme = 0

        if algoritma == "Genetik":
            rota = genetik_algoritma(drone, teslimatlar, noflyzones, saat)
        else:
            uygun_teslimatlar = [t for t in teslimatlar if teslimat_mumkun_mu(drone, t, noflyzones, saat)]
            rota = []
            for t in uygun_teslimatlar:
                yol = astar(drone, t.pos, noflyzones=noflyzones, teslimat=t)
                if yol:
                    ihlal_var_mi = False
                    for i in range(len(yol) - 1):
                        a, b = yol[i], yol[i + 1]
                        if cizgi_nofly_icinden_geciyor_mu(a, b, noflyzones, simdi_saat=saat):
                            ceza_adedi += 1
                            ihlal_var_mi = True
                            break

                    if not ihlal_var_mi:
                        rota.append(t)
                        mesafe = mesafe_hesapla(drone.start_pos, t.pos)
                        harcanan_enerji = t.weight * mesafe
                        drone.harca(harcanan_enerji)

                        if not drone.aktif:
                            drone.start_pos = (0, 0)
                            drone.battery = 10000
                            drone.aktif = True
                            toplam_bekleme += 5
                        else:
                            drone.start_pos = t.pos
                else:
                    ceza_adedi += 1

        bitis = time.time()

        tamamlanan = len([t for t in rota if teslimat_mumkun_mu(drone, t, noflyzones, saat)])
        yuzde = (tamamlanan / teslimat_sayisi) * 100 if teslimat_sayisi > 0 else 0
        ort_enerji = sum(t.weight * 5 for t in rota) / drone_sayisi
        sure = round(bitis - baslangic + toplam_bekleme, 2)
        ceza_puani = ceza_adedi * 1000

        sonuc_yazi = f"""✔️ Tamamlanan Teslimat: %{round(yuzde, 2)}\n⚡ Ortalama Enerji: {round(ort_enerji, 2)} birim\n❌ Ceza Puanı: {ceza_puani} ({ceza_adedi} ihlal)\n⏱️ Süre: {sure} saniye (şarj bekleme dahil)"""
        metrikler_label.config(text=sonuc_yazi)

        rota_ciz(drone, rota, noflyzones)

    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu:\n{e}")


# ------------------ ARAYÜZ BAŞLANGIÇ ---------------------
pencere = tk.Tk()
pencere.title("Drone Filo Simülasyonu")
pencere.geometry("420x480")

tk.Label(pencere, text="📦 Drone Filo Simülasyonu", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(pencere, text="Drone Sayısı:").pack()
entry_drone = tk.Entry(pencere)
entry_drone.pack()

tk.Label(pencere, text="Teslimat Sayısı:").pack()
entry_teslimat = tk.Entry(pencere)
entry_teslimat.pack()

tk.Label(pencere, text="No-Fly Zone Sayısı:").pack()
entry_nofly = tk.Entry(pencere)
entry_nofly.pack()

tk.Label(pencere, text="Simülasyon Saati (örn: 09:30):").pack()
entry_saat = tk.Entry(pencere)
entry_saat.pack()

tk.Label(pencere, text="Algoritma Seç:").pack()
secili_algoritma = tk.StringVar(value="Genetik")
tk.Radiobutton(pencere, text="Genetik Algoritma", variable=secili_algoritma, value="Genetik").pack()
tk.Radiobutton(pencere, text="A* Algoritması", variable=secili_algoritma, value="A*").pack()

tk.Button(pencere, text="Simülasyonu Başlat", command=baslat, bg="#009E49", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

metrikler_label = tk.Label(pencere, text="", justify="left", font=("Arial", 10))
metrikler_label.pack()

pencere.mainloop()

# --------- OPSİYONEL TEST (sabit graf ile örnek kullanım) ---------
graf = {
    'T0': [('T1', 10), ('T2', 15)],
    'T1': [('T0', 10), ('T3', 12), ('T4', 15)],
    'T2': [('T0', 15), ('T4', 10)],
    'T3': [('T1', 12), ('T5', 1)],
    'T4': [('T1', 15), ('T2', 10), ('T5', 5)],
    'T5': [('T3', 1), ('T4', 5)]
}

if __name__ == '__main__':
    yol = astar_static_graph(graf, 'T0', 'T5')
    print("En kısa yol:", yol)
