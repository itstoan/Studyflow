
from fastapi import HTTPException

from ..schemas.activity import (
    ActivityCreate,
    ActivityCreateResponse,
    ActivityInstanceRead,
    ActivityRead,
)


# Temporary in-memory storage.
# Data will be lost when the server process restarts.
_demo_activities: list[ActivityRead] = [
    ActivityRead(
        id=1,
        name="Ôn tập DSA",
        description="Ôn tập cấu trúc dữ liệu và giải thuật",
        default_priority="HIGH",
    ),
    ActivityRead(
        id=2,
        name="Đọc tài liệu Computer Networks",
        description=None,
        default_priority="MEDIUM",
    ),
]

_demo_instances: list[ActivityInstanceRead] = []


def list_activities() -> list[ActivityRead]:
    return _demo_activities


def create_activity(
    payload: ActivityCreate,
) -> ActivityCreateResponse:
    # Business rule: end time must be later than start time.
    if payload.end_time <= payload.start_time:
        raise HTTPException(
            status_code=422,
            detail="end_time must be later than start_time.",
        )

    # Temporary ID generation.
    # PostgreSQL will manage identity values later.
    next_id = max(
        (activity.id for activity in _demo_activities),
        default=0,
    ) + 1

    activity = ActivityRead(
        id=next_id,
        name=payload.name,
        description=payload.description,
        default_priority=payload.default_priority,
    )

    instance = ActivityInstanceRead(
        activity_id=next_id,
        series_position=1,
        name=payload.name,
        description=payload.description,
        priority=payload.default_priority,
        status="NOT_STARTED",
        schedule_date=payload.schedule_date,
        start_time=payload.start_time,
        end_time=payload.end_time,
        deadline_at=payload.deadline_at,
    )

    # Add both only after validation succeeds.
    _demo_activities.append(activity)
    _demo_instances.append(instance)

    return ActivityCreateResponse(
        activity=activity,
        instance=instance,
    )
