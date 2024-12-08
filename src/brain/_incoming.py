from .._utils._errors import AlreadyUnlockedError, AlreadyLockedError, NotParkingZoneError
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

def get_brain():
    """
    Returns the Brain instance.
    Injected at runtime via dependency override.
    """
    pass


class StartTripRequest(BaseModel):
    user_id: int

@app.post("/start_trip")
def start_trip(request: StartTripRequest, brain = Depends(get_brain)):
    try:
        brain.bike.unlock(request.user_id)
        brain.send_log()
        brain.send_report()
        return {"message": "Trip started. Log and report sent."}
    except AlreadyUnlockedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

class MoveRequest(BaseModel):
    longitude: float
    latitude: float

@app.post("/move")
def move(request: MoveRequest, brain = Depends(get_brain)):
    try:
        brain.bike.move(request.longitude, request.latitude)
        brain.send_report()
        return {"message": "Moved and battery drained. Report sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


class RelocateRequest(BaseModel):
    longitude: float
    latitude: float

@app.post("/relocate")
def relocate(request: RelocateRequest, brain = Depends(get_brain)):
    try:
        brain.bike.relocate(request.longitude, request.latitude)
        brain.send_report()
        return {"message": "Relocated. Report sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


class EndTripRequest(BaseModel):	
    ignore_zone: bool = False
    maintenance: bool = False

@app.post("/end_trip")
def end_trip(request: EndTripRequest, brain = Depends(get_brain)):
    try:
        brain.bike.lock(request.ignore_zone, request.maintenance)
        brain.send_log()
        brain.send_report()
        return {"message": "Trip ended. Log and report sent"}
    except AlreadyLockedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotParkingZoneError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


class CheckRequest(BaseModel):
    pass

@app.post("/check")
def check(request: CheckRequest, brain = Depends(get_brain)):
    try:
        brain.bike.check()
        brain.send_report()
        return {"message": "Bike checked. Report sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


class ReportRequest(BaseModel):
    pass

@app.get("/report")
def report(request: ReportRequest, brain = Depends(get_brain)):
    brain.bike.report()
    brain.send_report()
    return {"message": "Report created and sent"}


class UpdateRequest(BaseModel):
    pass

@app.post("/update")
def update(request: UpdateRequest, brain = Depends(get_brain)):
    zones = brain.request_zones()
    brain.bike.update(zones)
    return {"message": "Zones updated"}
