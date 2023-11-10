from grove.adc import ADC

class Sensor:
    '''Moisture Sensor class for reading the moisture value.'''
    def __init__(self, PIN):
        self.PIN = PIN
        self.aio = ADC()
    
       
    def moisture(self):
        self.moisture = self.aio.read(self.PIN)
        return self.moisture