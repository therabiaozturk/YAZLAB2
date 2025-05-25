import random
from csp import teslimat_mumkun_mu

# Fitness fonksiyonu – Raporla birebir uyumlu
def fitness_hesapla(rotalar, drone, noflyzones, saat):
    teslimat_sayisi = 0
    toplam_enerji = 0
    kural_ihlali = 0

    for teslimat in rotalar:
        if teslimat_mumkun_mu(drone, teslimat, noflyzones, saat):
            teslimat_sayisi += 1
            toplam_enerji += teslimat.weight * 5  # Enerji hesabı
        else:
            kural_ihlali += 1

    # Rapor formülüne göre fitness hesaplanır:
    # Fitness = (teslimat sayısı × 50) - (toplam enerji × 0.1) - (kural ihlali × 1000)
    fitness = (teslimat_sayisi * 50) - (toplam_enerji * 0.1) - (kural_ihlali * 1000)
    return fitness

# Rastgele başlangıç popülasyonu oluşturur
def rastgele_rota_uret(teslimatlar, adet):
    return [random.sample(teslimatlar, len(teslimatlar)) for _ in range(adet)]

# Crossover (çaprazlama) – İki rotadan yeni rota üretir
def crossover(rota1, rota2):
    nokta = random.randint(1, len(rota1)-2)
    yeni_rota = rota1[:nokta] + [t for t in rota2 if t not in rota1[:nokta]]
    return yeni_rota

# Mutasyon – İki teslimat noktasının yerini değiştirir
def mutation(rota):
    if len(rota) < 2:
        return rota
    i, j = random.sample(range(len(rota)), 2)
    rota[i], rota[j] = rota[j], rota[i]
    return rota

# Genetik algoritma ana fonksiyonu
def genetik_algoritma(drone, teslimatlar, noflyzones, saat, nesil_sayisi=50, pop_size=10):
    pop = rastgele_rota_uret(teslimatlar, pop_size)

    for nesil in range(nesil_sayisi):
        # Her rotanın fitness değeri hesaplanır
        skorlar = [(fitness_hesapla(rota, drone, noflyzones, saat), rota) for rota in pop]
        skorlar.sort(reverse=True, key=lambda x: x[0])
        en_iyiler = [r for _, r in skorlar[:4]]  # En iyi 4 rota seçilir

        yeni_pop = en_iyiler.copy()

        # Yeni nesil üretimi: crossover ve mutasyon
        while len(yeni_pop) < pop_size:
            r1, r2 = random.sample(en_iyiler, 2)
            yeni_rota = crossover(r1, r2)
            if random.random() < 0.3:  # %30 ihtimalle mutasyon uygula
                yeni_rota = mutation(yeni_rota)
            yeni_pop.append(yeni_rota)

        pop = yeni_pop

    # En iyi skora sahip rotayı döndür
    en_iyi_fitness, en_iyi_rota = max(
        [(fitness_hesapla(rota, drone, noflyzones, saat), rota) for rota in pop],
        key=lambda x: x[0]
    )
    return en_iyi_rota
