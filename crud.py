import json

import requests
from sqlalchemy.orm import Session
import models
import shemas


def get_user_notes(db: Session, user_id: int):
    result = db.query(models.Note).filter(models.Note.owner_id == user_id).all()
    return result


def create_user_note(db: Session, note: shemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    url_content = f'https://speller.yandex.net/services/spellservice.json/checkTexts?text={db_note.content}'
    url_title = f'https://speller.yandex.net/services/spellservice.json/checkTexts?text={db_note.title}'
    # r = requests.get(url_content)
    # response_json = json.loads(r.content)
    #
    # for suggestion in response_json[0]:
    #     db_note.content = db_note.content.replace(suggestion['word'], suggestion['s'][0])
    db_note.content = edittext(db_note.content, url_content)
    db_note.title = edittext(db_note.title, url_title)


    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def edittext(text, url):
    r = requests.get(url)
    response_json = json.loads(r.content)

    for suggestion in response_json[0]:
        text = text.replace(suggestion['word'], suggestion['s'][0])

    return text