class Drone:
    def __init__(self, id, max_weight, battery, speed, start_pos):
        self.id = id  
        self.max_weight = max_weight  
        self.battery = battery  
        self.speed = speed  
        self.start_pos = start_pos  
    
    def __repr__(self):
        return f"Drone#{self.id} - pos: {self.start_pos}, batarya: {self.battery} mAh"
