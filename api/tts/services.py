import base64
import random
import types

from gtts import gTTS
import os

from api.tts.repository import JujeobRepository
from util.logging_util import logger


def get(text):
    tts = gTTS(text=text, lang='ko')
    filename = f'{text}_voice.mp3'
    tts.save(filename)
    try:
        with open(filename, 'rb') as f:
            data = base64.b64encode(f.read()).decode('UTF-8')
            logger.info(f"data:::{data}")
            if os.path.exists(filename):
                os.remove(filename)
            return data
    except FileNotFoundError as e:
        raise Exception(f"File not found: {filename}")


def get_jujeob(name):
    jujeob = JujeobRepository(name)
    methods = [method_name for method_name, method in JujeobRepository.__dict__.items() if
               type(method) == property]
    random_method = getattr(jujeob, random.choice(methods))
    response = {}
    #response['voice'] = get(random_method)
    response['text'] = random_method
    return response
