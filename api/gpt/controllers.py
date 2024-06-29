from flask_restx import Resource, fields
from flask import  Response
from http import HTTPStatus

from multidict import MultiDict
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
        first = request.args
        return Response(generate_stream_response(first), content_type='text/event-stream')

# 스트리밍 함수
def generate_stream_response(initTalk: MultiDict, after :str = None):
    mbti = initTalk.get['mbti'] if initTalk.get('mbti') == None else 'INFP'
    messages= [{'role': 'user', 'content': f'너는 mbti의 {mbti} 성격을 가진 20대 여자인것 처럼 연기해줘 그리고 대답은 20글자를 넘지마, 그리고 신뢰도 라던지 뭐 이상한 답변 말고 그외의 것 넣지마'},
                  {'role': 'assistant', 'content': '웅 알겠어'},
                  {'role': 'user', 'content': initTalk.get('content')}]
    
    stream = ollama.chat(
        model='ggml',
        messages= messages,
        stream=True,
    )

    for chunk in stream:
        yield json.dumps({'message': chunk['message']['content']}) + '\n'