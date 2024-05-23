import argparse
import base64

from gtts import gTTS
import os
import playsound

from util.logging_util import logger


def get(text):
    tts = gTTS(text=text, lang='ko')
    filename = f'{text}_voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    try:
        with open(filename, 'rb') as f:
            data = base64.b64encode(f.read()).decode('UTF-8')
            logger.info(f"data:::{data}")
            if os.path.exists(filename):
                os.remove(filename)
            return data
    except FileNotFoundError as e:
        raise Exception(f"File not found: {filename}")
