
from datetime import date, datetime, time
from typing import Literal

from pydantic import BaseModel


class ActivityRead(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    default_priority: Literal["LOW", "MEDIUM", "HIGH"]


class ActivityCreate(BaseModel):
    name: str | None = None
    description: str | None = None
    default_priority: Literal["LOW", "MEDIUM", "HIGH"]

    schedule_date: date
    start_time: time
    end_time: time

    deadline_at: datetime | None = None


class ActivityInstanceRead(BaseModel):
    activity_id: int
    series_position: int

    name: str | None = None
    description: str | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"]
    status: Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]

    schedule_date: date
    start_time: time
    end_time: time
    deadline_at: datetime | None = None


class ActivityCreateResponse(BaseModel):
    activity: ActivityRead
    instance: ActivityInstanceRead
