from flask_restx import Namespace

tts_api = Namespace(name='tts', path='/tts', description='tts관련된 API 모음')