#from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
from app.enums import PriorityLevel



class Activity(Base):
    __tablename__ = "activities"

    activity_id: Mapped[int] = mapped_column(primary_key=True)
    activity_name: Mapped[str | None] 
    activity_description: Mapped[str | None] 
    activity_priority: Mapped[PriorityLevel]  = mapped_column(Enum(PriorityLevel, native_enum=False, create_constraint=True, name="activity_priority"), server_default=f'{PriorityLevel.MEDIUM.value}')
    #subject_id: Mapped[int] = mapped_column()
    #default_location: Mapped[str] = mapped_column(nullable=True)

    # __table_args__ = (
    #     CheckConstraint(
    #         "activity_priority in ('LOW', 'MEDIUM', 'HIGH')", name="activity_priority_check"
    #     ),
    # )
