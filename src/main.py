import asyncio
import os
import uvicorn
import platform
from dotenv import load_dotenv
from ._utils._errors import Errors
from ._utils._settings import Settings
from .brain.brain import Brain
from .brain._incoming import app, get_brain

load_dotenv()

print("DEBUG: BACKEND_URL =", os.getenv("BACKEND_URL"))
print("DEBUG: BIKE_ID =", os.getenv("BIKE_ID"))
print("DEBUG: TOKEN =", os.getenv("TOKEN"))
print("DEBUG: LONGITUDE =", os.getenv("LONGITUDE"))

def show_help():
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

async def main():
    bike_id = os.getenv("BIKE_ID")
    token = os.getenv("TOKEN")
    longitude = Settings.Position.default_longitude \
        if not os.getenv("LONGITUDE", "") else os.getenv("LONGITUDE")
    latitude = Settings.Position.default_latitude \
        if not os.getenv("LATITUDE", "") else os.getenv("LATITUDE")

    required = [bike_id, token]
    for environment_variable in required:
        if not environment_variable:
            show_help()
            raise Errors.initialization_error()

    brain = Brain(
        bike_id=bike_id,
        longitude=longitude,
        latitude=latitude,
        token=token
    )

    await brain.initialize()

    app.dependency_overrides[get_brain] = lambda: brain

    host = "0.0.0.0"
    if platform.system() == "Windows":
        host = "127.0.0.1"

    config = uvicorn.Config(
        app,
        host=host,
        port=8000 + int(bike_id),
        log_level="debug",
        loop="asyncio",
        lifespan="on"
    )
    server = uvicorn.Server(config)

    await asyncio.gather(
        brain.run(),
        server.serve()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Application has been shut down.")

# BIKE_ID=1 TOKEN=token python -m src.main

# TODO: Create Docker related files.
# TODO: Does authentication work as it is?
#       Token not through parameter but through
#       environment variable only in classes (Brain, Outgoing etc.)
# TODO: Utöka testning + uppdatera existerande tester i Bike.
# TODO: Ordna linting.
