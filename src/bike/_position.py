class Position:
    def __init__(self, longitude, latitude):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.current = (self.longitude, self.latitude)

    def change(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.current = (longitude, latitude)
