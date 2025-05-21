import matplotlib.pyplot as plt

def rota_ciz(drone, rota, noflyzones=None):
    fig, ax = plt.subplots()

    # Başlangıç noktası
    sx, sy = drone.start_pos
    ax.plot(sx, sy, 'bo', label='Başlangıç (Drone)')  # mavi nokta

    # Teslimat noktaları
    x = [t.pos[0] for t in rota]
    y = [t.pos[1] for t in rota]
    ax.plot(x, y, 'ro', label='Teslimatlar')  # kırmızı noktalar

    # Rota çizgisi (başlangıç + rota)
    full_x = [sx] + x
    full_y = [sy] + y
    ax.plot(full_x, full_y, 'k--', label='Rota')  # kesik çizgi

    # No-Fly Zone çizimi
    if noflyzones:
        for zone in noflyzones:
            coords = zone.coordinates + [zone.coordinates[0]]  # polygonu kapat
            zx = [c[0] for c in coords]
            zy = [c[1] for c in coords]
            ax.plot(zx, zy, 'r-', linewidth=1.5, label=f'No-Fly Zone#{zone.id}')

    ax.set_title(f"Drone#{drone.id} Rota Haritası")
    ax.set_xlabel("X Koordinatı")
    ax.set_ylabel("Y Koordinatı")
    ax.grid(True)
    ax.legend()
    plt.axis("equal")
    plt.show()
