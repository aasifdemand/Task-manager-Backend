from sqlalchemy.orm import Session
from models.task import Task, TaskStatus
from schemas.task import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    task_in: TaskCreate,
    owner_id: int
) -> Task:
    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        due_date=task_in.due_date,
        owner_id=owner_id,
        is_completed=task_in.status == TaskStatus.DONE
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Task)
        .filter(Task.owner_id == owner_id)
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )



def update_task(
    db: Session,
    task: Task,
    task_in: TaskUpdate
) -> Task:
    update_data = task_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    # keep consistency
    if task.status == TaskStatus.DONE:
        task.is_completed = True

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
