class NoFlyZone:
    def __init__(self, id, coordinates, active_time):
        self.id = id  
        self.coordinates = coordinates  # [(x1,y1), (x2,y2), ...] gibi çokgen köşeleri
        self.active_time = active_time  # (başlangıç, bitiş) saati

    def __repr__(self):
        return f"NoFlyZone#{self.id} - {len(self.coordinates)} köşe - Aktif: {self.active_time}"
