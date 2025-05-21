import random
from drone import Drone
from teslimat import Teslimat
from noflyzone import NoFlyZone

def drone_uret(adet):
    drones = []
    for i in range(adet):
        drone = Drone(
            id=i,
            max_weight=round(random.uniform(1.0, 5.0), 2),
            battery=random.randint(8000, 12000),
            speed=round(random.uniform(5.0, 15.0), 2),
            start_pos=(random.randint(0, 100), random.randint(0, 100))
        )
        drones.append(drone)
    return drones

def teslimat_uret(adet):
    teslimatlar = []
    for i in range(adet):
        teslimat = Teslimat(
            id=i,
            pos=(random.randint(0, 100), random.randint(0, 100)),
            weight=round(random.uniform(0.5, 4.0), 2),
            priority=random.randint(1, 5),
            time_window=("09:00", "11:00")  # sabit aralık, sonra dinamik yapabiliriz
        )
        teslimatlar.append(teslimat)
    return teslimatlar

def noflyzone_uret(adet):
    noflyzones = []
    for i in range(adet):
        # Kare gibi 4 köşeli bölge oluştur
        x = random.randint(20, 80)
        y = random.randint(20, 80)
        size = random.randint(5, 15)
        coordinates = [(x, y), (x+size, y), (x+size, y+size), (x, y+size)]
        nfz = NoFlyZone(
            id=i,
            coordinates=coordinates,
            active_time=("09:30", "10:30")
        )
        noflyzones.append(nfz)
    return noflyzones
