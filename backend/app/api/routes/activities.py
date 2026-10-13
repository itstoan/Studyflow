
from fastapi import APIRouter, status

from ...schemas.activity import (
    ActivityCreate,
    ActivityCreateResponse,
    ActivityRead,
)
from ...services import activity_service


router = APIRouter(tags=["Activities"])


@router.get(
    "/activities",
    response_model=list[ActivityRead],
)
def list_activities() -> list[ActivityRead]:
    return activity_service.list_activities()


@router.post(
    "/activities",
    response_model=ActivityCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_activity(
    payload: ActivityCreate,
) -> ActivityCreateResponse:
    return activity_service.create_activity(payload)
