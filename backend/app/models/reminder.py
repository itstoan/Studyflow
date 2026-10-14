from app.db.database import Base
from sqlalchemy import ForeignKey, Enum, ForeignKeyConstraint, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import TriggerType
from datetime import datetime

class Reminder(Base):
    __tablename__ = "reminders"

    reminder_id: Mapped[int] = mapped_column(primary_key=True)
    activity_id: Mapped[int] 
    series_position: Mapped[int]

    trigger_type: Mapped[TriggerType]  = mapped_column(Enum(TriggerType, native_enum = False, create_constraint = True, name = "trigger_type"))
    offset_minutes: Mapped[int] = mapped_column(nullable=False)

    enabled: Mapped[bool] = mapped_column(server_default='true')
    sent_at: Mapped[datetime | None]

    __table_args__ = (
        ForeignKeyConstraint(
            ["activity_id", "series_position"],
            ["activity_instances.activity_id", "activity_instances.series_position"],
            ondelete="CASCADE"
        ),
        CheckConstraint(
            "offset_minutes >= 0", name = "offset_minutes"
        ),
        UniqueConstraint(
            "activity_id", "series_position", "trigger_type", "offset_minutes",
            name = "same_triggers"
        ),
    )