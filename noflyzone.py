class NoFlyZone:
    def __init__(self, id, coordinates, active_time):
        self.id = id  
        self.coordinates = coordinates  # [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.active_time = active_time  # ("09:00", "10:00") gibi tuple

    def aktif_mi(self, simdi_saat):
        if not self.active_time:
            return True
        bas, bit = self.active_time
        return bas <= simdi_saat <= bit

    def __repr__(self):
        return f"NoFlyZone#{self.id} - {len(self.coordinates)} köşe - Aktif: {self.active_time}"
