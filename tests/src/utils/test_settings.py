from src._utils._settings import Settings

class TestBikesEndpoints:

    def test_get_all(self):
        expected = 'v1/bikes/'
        assert Settings.Endpoints.Bikes.get_all() == expected

    def test_get(self):
        bike_id = 123
        expected = f'v1/bikes/{bike_id}'
        assert Settings.Endpoints.Bikes.get(bike_id) == expected

    def test_add(self):
        expected = 'v1/bikes/'
        assert Settings.Endpoints.Bikes.add() == expected

    def test_update(self):
        bike_id = 456
        expected = f'v1/bikes/{bike_id}'
        assert Settings.Endpoints.Bikes.update(bike_id) == expected

    def test_remove(self):
        bike_id = 789
        expected = f'v1/bikes/{bike_id}'
        assert Settings.Endpoints.Bikes.remove(bike_id) == expected
