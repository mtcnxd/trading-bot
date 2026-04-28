from gpiozero import CPUTemperature

class Sensors:
    def __init__(self):
        self.cpu = CPUTemperature()
    
    def get_cpu_temperature(self):
        return round(self.cpu.temperature, 1)
