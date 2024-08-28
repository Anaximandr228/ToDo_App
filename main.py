import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import crud
import models
import serializer
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/users")
# def render_result():
#     todo_list = crud.get_note(db)
#     return {todo_list}

# @app.get("/notes", response_model=List[serializer.Note])
# def read_user(db: Session = Depends(get_db)):
#     db_user = crud.get_note(db)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.get("/users/{user_id}", response_model=serializer.Note)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_notes = crud.get_user_notes(db, user_id=user_id)
    if db_notes is None:
        raise HTTPException(status_code=404, detail="User not found")
    return list(db_notes)


@app.post("/users/{user_id}/notes/", response_model=serializer.Note)
def create_note_for_user(
        user_id: int, note: serializer.NoteCreate, db: Session = Depends(get_db)
):
    return crud.create_user_note(db=db, note=note, user_id=user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
