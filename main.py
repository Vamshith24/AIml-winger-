from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud

from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo List API")

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Todo API Running"}


@app.post("/todos", response_model=schemas.TodoResponse)
def create(todo: schemas.TodoCreate,
           db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.get("/todos")
def read_all(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@app.get("/todos/{todo_id}")
def read_one(todo_id: int,
             db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    return todo


@app.put("/todos/{todo_id}")
def update(todo_id: int,
           todo: schemas.TodoUpdate,
           db: Session = Depends(get_db)):
    updated = crud.update_todo(
        db,
        todo_id,
        todo
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    return updated


@app.delete("/todos/{todo_id}")
def delete(todo_id: int,
           db: Session = Depends(get_db)):
    deleted = crud.delete_todo(
        db,
        todo_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    return {"message": "Todo Deleted"}