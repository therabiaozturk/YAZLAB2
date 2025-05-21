class Teslimat:
    #uçuşa yasak bölgeler
    def __init__(self, id, pos, weight, priority, time_window):
        self.id = id  
        self.pos = pos  
        self.weight = weight  
        self.priority = priority  
        self.time_window = time_window  

    def __repr__(self):
        return f"Teslimat#{self.id} - {self.weight}kg - Öncelik: {self.priority}"
