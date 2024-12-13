class Position:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.current = (longitude, latitude)

    def change(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.current = (longitude, latitude)
