import asyncio
import os
import uvicorn
from typing import List
from dotenv import load_dotenv
from ._utils._errors import Errors
from ._utils._clock import Clock
from .brain._initialize import Initialize
from .brain.brain import Brain
from .brain.hivemind import Hivemind
from .brain._incoming import app

load_dotenv()

print("DEBUG: BACKEND_URL =", os.getenv("BACKEND_URL"))
print("DEBUG: BIKE_IDS =", os.getenv("BIKE_IDS"))
print("DEBUG: TOKEN =", os.getenv("TOKEN"))
print("DEBUG: POSITIONS =", os.getenv("POSITIONS"))

def show_help():
    print("""
            Required Environment Variables:
            - BIKE_IDS: Comma-separated list of bike IDs.
            - TOKEN: The API token.

            Optional Environment Variables:
            - POSITIONS: Comma-separated list of longitude:latitude pairs.
            If not provided, default positions will be used.
          
            Other Information:
            - BIKE_IDS and POSITIONS must be of the same length (or POSITIONS can be omitted).
          """)

# TODO: Configure logging and write logs to file (1 per bike_id/brain + 1 general log file).

async def main():
    TOKEN = os.getenv("TOKEN", "")
    INIT_BIKES_REMOTELY = os.getenv("INIT_BIKES_REMOTELY", "True").lower() == "true"
    if not INIT_BIKES_REMOTELY:
        print("DEBUG: Initializing bikes locally.")
        BIKE_IDS = os.getenv("BIKE_IDS", "")
        POSITIONS = os.getenv("POSITIONS", "")
    else:
        try:
            seconds_to_wait_for_backend = 5
            print(f"BIKE: Waiting {seconds_to_wait_for_backend} seconds in order for the backend to start.")
            await Clock.sleep(seconds_to_wait_for_backend)
            initialize = Initialize(TOKEN)
            BIKE_IDS = await initialize.bike_ids()
            POSITIONS = await initialize.bike_positions()
        except Exception as e:
            print(f"ERROR: Failed to initialize: {e}")
            print("Getting bike IDs and positions from environment variables instead.")

    if not BIKE_IDS:
        show_help()
        print("ERROR: BIKE_IDS is required.")
        raise Errors.initialization_error()

    try:
        BIKE_IDS: List[int] = [int(bike_id.strip()) for bike_id in BIKE_IDS.split(",")]
    except ValueError as e:
        show_help()
        print(f"ERROR: BIKE_IDS must be a comma-separated list of integers: {e}")
        raise Errors.initialization_error()

    if POSITIONS:
        POSITIONS = [position.strip() for position in POSITIONS.split(",")]
        if len(BIKE_IDS) != len(POSITIONS):
            show_help()
            print("ERROR: BIKE_IDS and POSITIONS must be of the same length.")
            raise Errors.initialization_error()
        try:
            POSITIONS = [tuple(map(float, position.split(":"))) for position in POSITIONS]
        except ValueError as e:
            show_help()
            print(f"ERROR: POSITIONS must be a comma-separated list of longitude:latitude pairs: {e}")
            raise Errors.initialization_error()

    if not POSITIONS:
        POSITIONS = list(zip([1.1] * len(BIKE_IDS), [1.1] * len(BIKE_IDS)))

    hivemind = Hivemind()

    brains = []
    for bike_id, (longitude, latitude) in zip(BIKE_IDS, POSITIONS):
        brain = Brain(
            bike_id=bike_id,
            longitude=longitude,
            latitude=latitude,
            token=TOKEN
        )
        await brain.initialize()
        hivemind.add_brain(bike_id, brain)
        brains.append(brain)

    app.state.hivemind = hivemind

    host = "0.0.0.0" # NOTE: This is for it to work in Docker.
    #if platform.system() == "Windows":
    #    host = "127.0.0.1"

    config = uvicorn.Config(
        app,
        host=host,
        port=8001,
        log_level="debug",
        loop="asyncio",
        lifespan="on"
    )
    server = uvicorn.Server(config)

    await asyncio.gather(
        *(brain.run() for brain in brains),
        server.serve()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Application has been shut down.")

# INIT_BIKES_REMOTELY=false BACKEND_URL='http://localhost:8000/' BIKE_IDS=1,2,3 TOKEN=token POSITIONS=13.45:54.124,13.46:54.125,13.47:54.126 python -m src.main
