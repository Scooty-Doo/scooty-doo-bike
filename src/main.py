import threading
import uvicorn
from ._utils._map import Map
from .brain.brain import Brain
from .brain._incoming import app, get_brain

if __name__ == "__main__":

    brain = Brain(
        bike_id="bike_9",
        longitude=100.0,
        latitude=100.0,
        token="token",
        zones=Map.Zones.load(),
    )

    def brain_thread():
        brain.run()

    def start_fastapi():
        def brain_dependency_override():
            return brain
        
        app.dependency_overrides[get_brain] = brain_dependency_override
        uvicorn.run(app, host="127.0.0.1", port=8000)

    brain_thread_instance = threading.Thread(target=brain_thread)
    brain_thread_instance.daemon = True
    brain_thread_instance.start()

    start_fastapi()

# python -m src.main