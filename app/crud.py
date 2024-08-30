import speller_service
from sqlalchemy.orm import Session
import models
import shemas


def get_user_notes(db: Session, user_id: int) -> models.Note:
    result = db.query(models.Note).filter(models.Note.owner_id == user_id).all()
    return result


def create_user_note(db: Session, note: shemas.NoteCreate, user_id: int) -> models.Note:
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db_note.content = speller_service.edittext(db_note.content)
    db_note.title = speller_service.edittext(db_note.title)
    db.add(db_note)
    db.commit()
    # db.refresh(db_note)
    return db_note


def create_user(db: Session, user: shemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
