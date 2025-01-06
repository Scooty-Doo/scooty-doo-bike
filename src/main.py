import asyncio
import os
import uvicorn
import time
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
    token = os.getenv("TOKEN", "")
    bike_ids = os.getenv("BIKE_IDS", "")
    positions = os.getenv("POSITIONS", "")
    try:
        print("BIKE: Waiting 10 seconds in order for the backend to start.")
        await Clock.sleep(10)
        initialize = Initialize(token)
        bike_ids = initialize.bike_ids()
        positions = initialize.bike_positions()
    except Exception as e:
        print(f"ERROR: Failed to initialize: {e}")
        print("Getting bike IDs and positions from environment variables instead.")

    if not bike_ids:
        show_help()
        print("ERROR: BIKE_IDS is required.")
        raise Errors.initialization_error()
    
    try:
        bike_ids: List[int] = [int(bike_id.strip()) for bike_id in bike_ids.split(",")]
    except ValueError as e:
        show_help()
        print(f"ERROR: BIKE_IDS must be a comma-separated list of integers: {e}")
        raise Errors.initialization_error()

    if positions:
        positions = [position.strip() for position in positions.split(",")]
        if len(bike_ids) != len(positions):
            show_help()
            print("ERROR: BIKE_IDS and POSITIONS must be of the same length.")
            raise Errors.initialization_error()
        try:
            positions = [tuple(map(float, position.split(":"))) for position in positions]
        except ValueError as e:
            show_help()
            print(f"ERROR: POSITIONS must be a comma-separated list of longitude:latitude pairs: {e}")
            raise Errors.initialization_error()

    if not positions:
        positions = list(zip([1.1] * len(bike_ids), [1.1] * len(bike_ids)))

    hivemind = Hivemind()

    brains = []
    for bike_id, (longitude, latitude) in zip(bike_ids, positions):
        brain = Brain(
            bike_id=bike_id,
            longitude=longitude,
            latitude=latitude,
            token=token
        )
        await brain.initialize()
        hivemind.add_brain(bike_id, brain)
        brains.append(brain)
    
    app.state.hivemind = hivemind # NOTE: Will this work? Or dependency injection is needed?

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

# BIKE_IDS=1,2,3 TOKEN=token POSITIONS=13.45:54.124,13.46:54.125,13.47:54.126 python -m src.main

# TODO: Create Docker related files.
