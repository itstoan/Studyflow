from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, ForeignKey, CheckConstraint
from app.enums import PriorityLevel, StatusLevel
from datetime import date, time, datetime

class ActivityInstance(Base):
    __tablename__ = "activity_instances"

    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.activity_id", ondelete="CASCADE"), primary_key=True)
    series_position: Mapped[int] = mapped_column(primary_key=True)

    activity_inst_name: Mapped[str | None] 
    activity_inst_description: Mapped[str | None] 
    activity_inst_priority: Mapped[PriorityLevel]  = mapped_column(
        Enum(PriorityLevel, native_enum=False, create_constraint=True, name="act_inst_priority"), 
        server_default=f'{PriorityLevel.MEDIUM.value}'
    )
    activity_inst_status: Mapped[StatusLevel]  = mapped_column(
        Enum(StatusLevel, native_enum=False, create_constraint=True, name="act_inst_status"), 
        server_default=f'{StatusLevel.NOT_STARTED.value}'
    )


    activity_inst_date: Mapped[date] = mapped_column(nullable=False)
    activity_inst_start_time: Mapped[time] = mapped_column(nullable=False)
    activity_inst_end_time: Mapped[time] = mapped_column(nullable=False)
    activity_inst_deadline: Mapped[datetime | None]

    schedule_exception: Mapped[bool] = mapped_column(server_default='false')

    __table_args__ = (
        CheckConstraint(
            "activity_inst_end_time > activity_inst_start_time", 
            name="time_range_validity" 
        ),
        CheckConstraint(
            "series_position >= 1", 
            name = "series_position"
        ), 
    )