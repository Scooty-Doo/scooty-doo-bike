class Position:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.current = (longitude, latitude)

    # TODO: currently not used, remove?
    def move(self, delta_long, delta_lat):
        self.longitude += delta_long
        self.latitude += delta_lat
        self.current = (self.longitude, self.latitude)

    def change(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.current = (longitude, latitude)
