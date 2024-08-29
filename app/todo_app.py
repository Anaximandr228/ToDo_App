from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import models, crud
import shemas
from app.database import engine, SessionLocal
from fastapi.security import HTTPBasic, HTTPBasicCredentials

models.Base.metadata.create_all(bind=engine)

security = HTTPBasic()
app = FastAPI(dependencies=[Depends(security)])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_id}", response_model=list[shemas.Note])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_notes = crud.get_user_notes(db, user_id=user_id)
    if db_notes is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_notes


@app.post("/users/{user_id}/notes/", response_model=shemas.Note)
def create_note_for_user(
    user_id: int, note: shemas.NoteCreate, db: Session = Depends(get_db)
):
    return crud.create_user_note(db=db, note=note, user_id=user_id)


users = {
    "admin": {
        "password": "Password123",
        "token": "",
        "priviliged": True
    }
}


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username
    user = users.get(current_username_bytes)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not credentials.password == user['password']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/user/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
