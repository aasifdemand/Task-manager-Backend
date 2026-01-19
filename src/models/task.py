from config.database import Base
from sqlalchemy import Column, Integer, String,Text,Enum, Boolean,DateTime,func,Index
import enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(
        Enum(TaskStatus, name="task_status",create_type=False),
        nullable=False,
        default=TaskStatus.TODO
        
    )
    
    is_completed = Column(Boolean, nullable=False, default=False)

    due_date = Column(DateTime(timezone=True), nullable=True)

    owner_id = Column(
    Integer,
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False
    )

    owner = relationship("User", back_populates="tasks")


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

Index("ix_tasks_status", Task.status)
Index("ix_tasks_due_date", Task.due_date)