class Validate:

    @staticmethod
    def is_valid_position(position):
        if not isinstance(position, (list, tuple)):
            return False
        if len(position) != 2:
            return False
        if not all(isinstance(coordinates, (int, float)) for coordinates in position):
            return False
        return True
    
    @staticmethod
    def is_valid_linestring(linestring):
        if not isinstance(linestring, list):
            return False
        if not all(isinstance(position, (list, tuple)) for position in linestring):
            return False
        if not all(len(position) == 2 for position in linestring):
            return False
        if not all(Validate.is_valid_position(position) for position in linestring):
            return False
        return True