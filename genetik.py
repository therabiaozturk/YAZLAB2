import random
from csp import teslimat_mumkun_mu

def fitness_hesapla(rotalar, drone, noflyzones, saat):
    toplam_puan = 0
    toplam_enerji = 0
    kural_ihlali = 0

    for teslimat in rotalar:
        if teslimat_mumkun_mu(drone, teslimat, noflyzones, saat):
            toplam_puan += 10 + teslimat.priority
            toplam_enerji += teslimat.weight * 5  # örnek enerji hesabı
        else:
            kural_ihlali += 1
            toplam_puan -= 5

    return toplam_puan - (toplam_enerji * 0.5) - (kural_ihlali * 10)

def rastgele_rota_uret(teslimatlar, adet):
    return [random.sample(teslimatlar, len(teslimatlar)) for _ in range(adet)]

def crossover(rota1, rota2):
    nokta = random.randint(1, len(rota1)-2)
    yeni = rota1[:nokta] + [t for t in rota2 if t not in rota1[:nokta]]
    return yeni

def mutation(rota):
    if len(rota) < 2:
        return rota
    i, j = random.sample(range(len(rota)), 2)
    rota[i], rota[j] = rota[j], rota[i]
    return rota

def genetik_algoritma(drone, teslimatlar, noflyzones, saat, nesil_sayisi=50, pop_size=10):
    pop = rastgele_rota_uret(teslimatlar, pop_size)

    for nesil in range(nesil_sayisi):
        skorlar = [(fitness_hesapla(rota, drone, noflyzones, saat), rota) for rota in pop]
        skorlar.sort(reverse=True, key=lambda x: x[0])
        en_iyiler = [r for _, r in skorlar[:4]]  # ilk 4 en iyi

        yeni_pop = en_iyiler.copy()

        while len(yeni_pop) < pop_size:
            r1, r2 = random.sample(en_iyiler, 2)
            yeni_rota = crossover(r1, r2)
            if random.random() < 0.3:
                yeni_rota = mutation(yeni_rota)
            yeni_pop.append(yeni_rota)

        pop = yeni_pop

    en_iyi_fitness, en_iyi_rota = max([(fitness_hesapla(rota, drone, noflyzones, saat), rota) for rota in pop], key=lambda x: x[0])
    return en_iyi_rota
