from flask_restx import Namespace

gpt_api = Namespace(name='gpt', path='/gpt', description='gpt관련된 API 모음')