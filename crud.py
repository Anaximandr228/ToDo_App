from sqlalchemy.orm import Session
import models
import serializer


def get_user_notes(db: Session, user_id: int):
    result = db.query(models.Note).filter(models.Note.owner_id == user_id).all()
    return [dict(r.__dict__) for r in result]

def create_user_note(db: Session, note: serializer.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note