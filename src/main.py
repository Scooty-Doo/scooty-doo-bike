import threading
import os
import uvicorn
from ._utils._errors import Errors
from ._utils._settings import Settings
from .brain.brain import Brain
from .brain._incoming import app, get_brain

def help():
    print("""
            Required Environment Variables:
            - BIKE_ID: The ID of the bike.
            - TOKEN: The API token.

            Optional Environment Variables:
            - LONGITUDE: The longitude of the bike's starting position. (Note: Bike can deploy itself.)
            - LATITUDE: The latitude of the bike's starting position. (Note: Bike can deploy itself.)
          
            Other Information:
            - srd/_utils/_zones.json: The zones file contains default zones for the map 
                (and should probably be included in Docker container).
            - same for _utils/_parking_zones.json
          """)

# TODO: Gör så att den tankar in miljövariabler från .env som default.
# men kan överskrivas med CLI?

if __name__ == "__main__":
    bike_id = os.getenv("BIKE_ID")
    longitude = Settings.Position.default_longitude if not os.getenv("LONGITUDE", "") else os.getenv("LONGITUDE")
    latitude = Settings.Position.default_latitude if not os.getenv("LATITUDE", "") else os.getenv("LATITUDE")
    token = os.getenv("TOKEN")

    required = [bike_id, token]
    for environment_variable in required:
        if not environment_variable:
            help()
            raise Errors.initialization_error()

    # TODO: Should token be skipped as parameter and instead taken from environment? Same on Outgoing?
    brain = Brain(
        bike_id=bike_id,
        longitude=longitude,
        latitude=latitude,
        token=token
    )

    def brain_thread():
        brain.run()

    def start_fastapi():
        def brain_dependency_override():
            return brain
        
        app.dependency_overrides[get_brain] = brain_dependency_override
        port = 8000 + int(bike_id)
        uvicorn.run(app, host="0.0.0.0", port=port)

    brain_thread_instance = threading.Thread(target=brain_thread)
    brain_thread_instance.daemon = True
    brain_thread_instance.start()

    start_fastapi()

# BIKE_ID=1 TOKEN=token python -m src.main

# TODO: Create Docker related files.
# TODO: Does authentication work as it is? Token not through parameter but through environment variable only in classes (Brain, Outgoing etc.)
# TODO: Utöka testning + uppdatera existerande tester i Bike.
# TODO: Ordna linting.