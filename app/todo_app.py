from typing import Annotated
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import models
import crud
import shemas
from database import engine, SessionLocal
from fastapi.security import HTTPBasic, HTTPBasicCredentials

models.Base.metadata.create_all(bind=engine)

security = HTTPBasic()
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_id(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)], db: Session = Depends(get_db)) -> int:
    current_username_bytes = credentials.username
    user = db.query(models.User).filter(models.User.username == current_username_bytes).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not credentials.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.id


@app.get("/notes", response_model=list[shemas.Note])
def read_notes(user_id: Annotated[int, Depends(get_user_id)], db: Session = Depends(get_db)):
    db_notes = crud.get_user_notes(db, user_id=user_id)
    if db_notes is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_notes


@app.post("/user/register", response_model=shemas.User)
def create_user(user: shemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/note", response_model=shemas.Note)
def create_note_for_user(user_id: Annotated[int, Depends(get_user_id)],
                         note: shemas.NoteCreate, db: Session = Depends(get_db)
                         ):
    return crud.create_user_note(db=db, note=note, user_id=user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
