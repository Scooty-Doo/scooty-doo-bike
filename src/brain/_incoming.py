"""
This module handles all the incoming requests to the bike hivemind API.
"""

from typing import Union, Optional
import asyncio
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, Query, Request, BackgroundTasks
from .brain import Brain
from .hivemind import Hivemind
from .._utils._errors import (AlreadyUnlockedError,
                              AlreadyLockedError,
                              InvalidPositionError,
                              MovingOrChargingError)

app = FastAPI()

def get_hivemind(request: Request) -> Hivemind:
    """Dependency to retrieve the Hivemind instance from the FastAPI app's state."""
    hivemind = request.app.state.hivemind
    if not hivemind:
        raise HTTPException(status_code=500, detail="Hivemind not initialized.")
    return hivemind

def get_brain(bike_id: Optional[int] = Query(
        None, description="The ID of the target bike."
        "Defaults to the lowest bike_id."),
        hivemind: Hivemind = Depends(get_hivemind)
        ) -> Brain:
    """Dependency to retrieve a Brain instance from the Hivemind instance."""
    try:
        return hivemind.get_brain(bike_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.get("/")
async def root():
    """Root endpoint of the API."""
    return {"message": "Welcome to the bike hivemind API."}

class StartTripRequest(BaseModel):
    """Request model for starting a trip."""
    user_id: int
    trip_id: int

@app.post("/start_trip")
async def start_trip(request: StartTripRequest, brain = Depends(get_brain)):
    """Handling incoming request to start a trip."""
    try:
        if brain.bike.is_moving_or_charging():
            raise MovingOrChargingError()
        brain.bike.unlock(request.user_id, request.trip_id)
        return {
            "message": "Trip started.",
            "data": {
                "report": brain.bike.reports.last(),
                "log": brain.bike.logs.last()}}
    except AlreadyUnlockedError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except MovingOrChargingError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Details: {e}") from e

class MoveRequest(BaseModel):
    """Request model for moving the bike."""
    position_or_linestring: Union[tuple, list[tuple]]

@app.post("/move")
async def move(
    request: MoveRequest,
    background_tasks: BackgroundTasks, # pylint: disable=unused-argument
    brain = Depends(get_brain)
    ):
    """Handling incoming request to move the bike."""
    try:
        if brain.bike.is_moving_or_charging():
            raise MovingOrChargingError()
        asyncio.create_task(brain.bike.move(request.position_or_linestring))
        return {
            "message": "Move initiated. Battery drain and reporting will be done during the move.",
            "data": {
                "report": brain.bike.reports.last()}}
    except AlreadyLockedError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except InvalidPositionError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except MovingOrChargingError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Details: {e}") from e


class RelocateRequest(BaseModel):
    """Request model for relocating the bike."""
    position: Union[tuple, list]

@app.post("/relocate")
async def relocate(request: RelocateRequest, brain = Depends(get_brain)):
    """Handling incoming request to relocate the bike."""
    try:
        if brain.bike.is_moving_or_charging():
            raise MovingOrChargingError()
        brain.bike.relocate(request.position)
        return {
            "message": "Relocated. Report sent.", 
            "data": {
                "report": brain.bike.reports.last()}}
    except AlreadyLockedError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except InvalidPositionError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except MovingOrChargingError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Details: {e}") from e


class EndTripRequest(BaseModel):
    """Request model for ending a trip."""
    maintenance: bool = False
    ignore_zone: bool = True

@app.post("/end_trip")
async def end_trip(request: EndTripRequest, brain = Depends(get_brain)):
    """Handling incoming request to end a trip."""
    try:
        if brain.bike.is_moving_or_charging():
            raise MovingOrChargingError()
        brain.bike.lock(request.maintenance, request.ignore_zone)
        return {
            "message": "Trip ended. Log and report sent",
            "data": {
                "log": brain.bike.logs.last(),
                "report": brain.bike.reports.last()}}
    except AlreadyLockedError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except MovingOrChargingError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Details: {e}") from e


class CheckRequest(BaseModel):
    """Request model for checking the bike."""
    maintenance: bool = False

@app.post("/check")
async def check(request: CheckRequest, brain = Depends(get_brain)):
    """Handling incoming request to check the bike."""
    try:
        if brain.bike.is_moving_or_charging():
            raise MovingOrChargingError()
        brain.bike.check(request.maintenance)
        return {
            "message": "Bike checked. Report sent",
            "data": {
                "report": brain.bike.reports.last()}}
    except MovingOrChargingError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Details: {e}") from e


class ReportRequest(BaseModel):
    """Request model for creating a report."""

@app.get("/report")
async def report(brain = Depends(get_brain)): # request: ReportRequest
    """Handling incoming request to create a report."""
    try:
        brain.bike.report()
        return {
            "message": "Report created and sent",
            "data": {
                "report": brain.bike.reports.last()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Details: {e}") from e

class LogRequest(BaseModel):
    """Request model for fetching a log."""

@app.get("/log")
async def log(brain = Depends(get_brain)):
    """Handling incoming request to fetch the last log."""
    try:
        return {
            "message": "Log created and sent",
            "data": {
                "log": brain.bike.logs.last()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Details: {e}") from e

class UpdateRequest(BaseModel):
    """Request model for updating the bike's zones and zone types."""

@app.post("/update")
async def update(brain = Depends(get_brain)): # request: UpdateRequest
    """Handling incoming request to update the bike's zones and zone types."""
    try:
        if brain.bike.is_moving_or_charging():
            raise MovingOrChargingError()
        zones = await brain.request_zones()
        zone_types = await brain.request_zone_types()
        brain.bike.update(zones=zones, zone_types=zone_types)
        return {"message": "Zones and zone types updated"}
    except MovingOrChargingError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Details: {e}") from e
