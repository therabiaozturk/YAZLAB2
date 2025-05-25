import heapq
import math

def mesafe_hesapla(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def astar(drone, hedef, noflyzones=[], teslimat=None):
    start = drone.start_pos
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)

        if current == hedef:
            yol = [current]
            while current in came_from:
                current = came_from[current]
                yol.append(current)
            yol.reverse()
            return yol

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                komsu = (current[0] + dx, current[1] + dy)

                if komsu[0] < 0 or komsu[0] > 100 or komsu[1] < 0 or komsu[1] > 100:
                    continue

                # ✅ Sadece nokta değil, çizgi üzerinden geçişi kontrol et
                if cizgi_nofly_icinden_geciyor_mu(current, komsu, noflyzones):
                    continue

                tahmini_g = g_score[current] + mesafe_hesapla(current, komsu)
                if komsu not in g_score or tahmini_g < g_score[komsu]:
                    came_from[komsu] = current
                    g_score[komsu] = tahmini_g
                    h = mesafe_hesapla(komsu, hedef)
                    f = tahmini_g + h
                    heapq.heappush(open_set, (f, komsu))
    return None  # yol bulunamadı

def astar_static_graph(graf, baslangic, hedef):
    open_set = []
    heapq.heappush(open_set, (0, baslangic))
    came_from = {}
    g_score = {node: float("inf") for node in graf}
    g_score[baslangic] = 0

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == hedef:
            yol = [current]
            while current in came_from:
                current = came_from[current]
                yol.append(current)
            yol.reverse()
            return yol

        for komsu, maliyet in graf[current]:
            tentative_g = g_score[current] + maliyet
            if tentative_g < g_score[komsu]:
                came_from[komsu] = current
                g_score[komsu] = tentative_g
                f_score = tentative_g
                heapq.heappush(open_set, (f_score, komsu))

    return None

# ✅ Nokta yasak bölge içinde mi (mevcut kontrol)
def noktada_yasak_var_mi(nokta, noflyzones):
    x, y = nokta
    for zone in noflyzones:
        xs = [c[0] for c in zone.coordinates]
        ys = [c[1] for c in zone.coordinates]
        if min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys):
            return True
    return False

# ✅ Yeni: Bir çizgi yasak bölgeden geçiyor mu?
# Güncellenmiş cizgi_nofly_icinden_geciyor_mu fonksiyonu
# Bu fonksiyon iki nokta arasındaki çizginin no-fly zone dikdörtgenlerinden herhangi biriyle kesilip kesilmediğini kontrol eder

def cizgi_nofly_icinden_geciyor_mu(a, b, noflyzones):
    def cakisiyor(p1, p2, rect):
        # Dört kenar için kontrol et (sol-sağ-üst-alt)
        kenarlar = [
            (rect[0], rect[1], rect[2], rect[1]),  # alt
            (rect[0], rect[3], rect[2], rect[3]),  # üst
            (rect[0], rect[1], rect[0], rect[3]),  # sol
            (rect[2], rect[1], rect[2], rect[3])   # sağ
        ]

        for x1, y1, x2, y2 in kenarlar:
            if kesisiyor_mu(p1, p2, (x1, y1), (x2, y2)):
                return True
        return False

    def kesisiyor_mu(p1, p2, q1, q2):
        # Yardımcı fonksiyon: iki çizgi parçası kesiyor mu
        def ccw(a, b, c):
            return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])

        return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))

    for zone in noflyzones:
        xs = [c[0] for c in zone.coordinates]
        ys = [c[1] for c in zone.coordinates]
        dikdortgen = (min(xs), min(ys), max(xs), max(ys))

        if cakisiyor(a, b, dikdortgen):
            return True
    return False

