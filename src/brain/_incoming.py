from .._utils._errors import AlreadyUnlockedError, AlreadyLockedError, InvalidPositionError
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from typing import Union

app = FastAPI(debug=True)

def get_brain():
    """
    Returns the Brain instance.
    Injected at runtime via dependency override.
    """
    pass


class StartTripRequest(BaseModel):
    user_id: int
    trip_id: int

@app.post("/start_trip")
def start_trip(request: StartTripRequest, brain = Depends(get_brain)):
    try:
        brain.bike.unlock(request.user_id, request.trip_id)
        return {
            "message": "Trip started.",
            "data": {
                "report": brain.bike.reports.last(),
                "log": brain.bike.logs.last()}}
    except AlreadyUnlockedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

class MoveRequest(BaseModel):
    position_or_linestring: Union[tuple, list[tuple]]

# TODO: gör så att den kan hantera tuple + Point WKR + list[tuple] + LineString WKR
@app.post("/move")
def move(request: MoveRequest, brain = Depends(get_brain)):
    try:
        brain.bike.move(request.position_or_linestring)
        return {
            "message": "Moved and battery drained. Report sent.",
            "data": {
                "report": brain.bike.reports.last()}}
    except AlreadyLockedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidPositionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


class RelocateRequest(BaseModel):
    longitude: float
    latitude: float

@app.post("/relocate")
def relocate(request: RelocateRequest, brain = Depends(get_brain)):
    try:
        brain.bike.relocate(request.longitude, request.latitude)
        return {
            "message": "Relocated. Report sent.", 
            "data": {
                "report": brain.bike.reports.last()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


class EndTripRequest(BaseModel):	
    maintenance: bool = False
    ignore_zone: bool = True

@app.post("/end_trip")
def end_trip(request: EndTripRequest, brain = Depends(get_brain)):
    try:
        brain.bike.lock(request.maintenance, request.ignore_zone)
        return {
            "message": "Trip ended. Log and report sent",
            "data": {
                "log": brain.bike.logs.last(),
                "report": brain.bike.reports.last()}}
    except AlreadyLockedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


class CheckRequest(BaseModel):
    pass

@app.post("/check")
def check(request: CheckRequest, brain = Depends(get_brain)):
    try:
        brain.bike.check()
        return {
            "message": "Bike checked. Report sent",
            "data": {
                "report": brain.bike.reports.last()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


class ReportRequest(BaseModel):
    pass

@app.get("/report")
def report(request: ReportRequest, brain = Depends(get_brain)):
    brain.bike.report()
    return {
        "message": "Report created and sent",
        "data": {
            "report": brain.bike.reports.last()}}


class UpdateRequest(BaseModel):
    pass

@app.post("/update")
def update(request: UpdateRequest, brain = Depends(get_brain)):
    zones = brain.request_zones()
    zone_types = brain.request_zone_types()
    brain.bike.update(zones=zones, zone_types=zone_types)
    return {"message": "Zones and zone types updated"}
