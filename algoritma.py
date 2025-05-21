import heapq
import math

def mesafe_hesapla(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def astar(drone, hedef, noflyzones=[]):
    start = drone.start_pos
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)

        if current == hedef:
            # Rota bulundu
            yol = [current]
            while current in came_from:
                current = came_from[current]
                yol.append(current)
            yol.reverse()
            return yol

        # Komşu noktaları üret (x, y ±1)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                komsu = (current[0] + dx, current[1] + dy)

                if komsu[0] < 0 or komsu[0] > 100 or komsu[1] < 0 or komsu[1] > 100:
                    continue  # alan dışında

                if noktada_yasak_var_mi(komsu, noflyzones):
                    continue  # no-fly zone

                tahmini_g = g_score[current] + mesafe_hesapla(current, komsu)
                if komsu not in g_score or tahmini_g < g_score[komsu]:
                    came_from[komsu] = current
                    g_score[komsu] = tahmini_g
                    h = mesafe_hesapla(komsu, hedef)
                    f = tahmini_g + h
                    heapq.heappush(open_set, (f, komsu))
    
    return None  # yol bulunamadı

def noktada_yasak_var_mi(nokta, noflyzones):
    x, y = nokta
    for zone in noflyzones:
        xs = [c[0] for c in zone.coordinates]
        ys = [c[1] for c in zone.coordinates]
        if min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys):
            return True
    return False
