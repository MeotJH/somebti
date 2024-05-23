from flask_restx import Resource, fields
from flask import  Response
from http import HTTPStatus
from api import gpt_api as api
import ollama
from flask import request
import json

tts_text_field = fields.String(required=True, title='tts 텍스트 데이터', description="TTS 바이너리로 변환된")

users_response_model = api.model('TTSResponseModel', {
    #'voice': binary_field,
    'text' : tts_text_field,
})

@api.route('/', strict_slashes=False)
class TTS(Resource):
    @api.doc(params={'name': 'Hello World'})
    def get(self):
        content = request.args.get('name')
        return Response(generate_stream_response(content), content_type='text/event-stream')

# 스트리밍 함수
def generate_stream_response(content: str):
    stream = ollama.chat(
        model='ggml',
        messages=[{'role': 'user', 'content': content}],
        stream=True,
    )

    for chunk in stream:
        yield json.dumps({'message': chunk['message']['content']}) + '\n'