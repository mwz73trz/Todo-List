from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    results = db.query(models.Task).all()
    print(results)
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Task)
def create_tasks(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{id}", response_model=schemas.Task)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found!")
    return task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    task = task_query.first()
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} does not exist!")
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Task)
def update_task(id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    task = task_query.first()
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} does not exist!")
    task_query.update(updated_task.dict(), synchronize_session=False)
    db.commit()
    return task_query.first()
 