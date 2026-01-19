from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from repositories.task_repository import (
    create_task,
    get_task,
    get_tasks,
    update_task,
    delete_task
)
from schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)
from dependencies.auth import get_current_user
from models.user import User


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)


@router.post("", response_model=TaskResponse, status_code=201)
def create_task_api(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task(db, task_in, owner_id=current_user.id)



@router.get(
    "",
    response_model=list[TaskResponse]
)
def list_tasks_api(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tasks(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit
    )



@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task_api(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task_api(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return update_task(db, task, task_in)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task_api(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    delete_task(db, task)
