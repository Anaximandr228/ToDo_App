import json

import requests


def edittext(text):
    r = requests.get(f'https://speller.yandex.net/services/spellservice.json/checkTexts?text={text}')
    response_json = json.loads(r.content)

    for suggestion in response_json[0]:
        text = text.replace(suggestion['word'], suggestion['s'][0])

    return text
