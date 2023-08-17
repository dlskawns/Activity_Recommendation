
import os
from langchain.callbacks import get_openai_callback
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

import time
 
# API 키설정
OPENAI_API_KEY = "Key"
#구글검색하려면 SERPAPI 필요(월 100회 무료/월 5000회 $50/월 15000회 $130/월 30000회 $250)
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


class Act_Rec:
    """
    일반 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 chatGPT기반 활동 및 질문 추천
    도서 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 도서추천API 로직 이후 csv에서 뽑아온 도서요약 건 관련 질문 추천 
    """
    def __init__(self):
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.8)
        self.response_schemas= [
            ResponseSchema(name="S1", description="탐구를 위한 에세이 주제. 질문이 아닌 주제를 출력 해야해"),
            ResponseSchema(name="Q1", description="첫번째 가이드 질문"),
            ResponseSchema(name="Q2", description="두번째 가이드 질문"),
            ResponseSchema(name="Q3", description="세번째 가이드 질문")
            ]
        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        self.format_instructions = self.output_parser.get_format_instructions()

    def general_recommend(self, major):
        """
        일반 관심분야 활동추천 기능
        major: 사용자의 입력값 - 관심분야
        """
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(
                "{major}에 대해 고등학생이 작성할 만한 탐구 주제 1개와 가이드 질문 3개를 진로상담가 처럼 출력해줘\n{format_instructions}"
                )],                                                             # GPT에게 하달할 프롬프트
            input_variables=["major"],                                          # 프롬프트 상의 변수 값
            partial_variables={"format_instructions": self.format_instructions} # 출력되는 포맷 입력
            )
        _input = prompt.format_prompt(major=major)                             # 유저 input값 입력
        with get_openai_callback() as cb:                                       # with 내 콜백 사항 answer 계산 제외 모두 삭제해도 됨
            print('일반 활동 추천 시작')
            # 시간 측정
            start = time.time()
            answer = self.llm(_input.to_messages())
            if answer.content.split('\n\t')[1].strip()[-1] != ',':
                print('에러발생------------------')
                answer.content = ','.join(answer.content.split('\n\t')).replace(',','', 1)

            print("answer type:", type(answer))
            print("answer:", answer)
            answer = self.output_parser.parse(answer.content)
            end = time.time()

            print(answer)
            print('일반 활동 추천 완료')
            print(cb)
            print(end-start, '경과\n---------------------------------------------------')
        return answer

    def book_recommend(self, major, book_text):
        """
        도서 활동추천 기능
        major: 사용자의 입력값 - 관심분야
        book_text: 사용자의 입력값에 따라 추천 API를 돌고 나온 추천 도서의 내용 요약 정보
        """
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(
                "{major}와 책 요약 정보를 연결지어 고등학생이 작성할 만한 탐구 주제 1개와 가이드 질문 3개를 진로상담가 처럼 출력해줘\n{format_instructions}\n책 요약:{book_text}"
                )],                                                             # GPT에게 하달할 프롬프트
            input_variables=["major", "book_text"],                             # 프롬프트 상의 입력 변수 값
            partial_variables={"format_instructions": self.format_instructions} # 출력되는 포맷을 변수로 입력
            )
        _input = prompt.format_prompt(major=major, book_text=book_text)         # 유저 input값(major) & 도서추천 결과 책요약(book_text) 입력
        with get_openai_callback() as cb:                                       # with 내 콜백 사항 answer 제외 모두 삭제해도 됨
            # 시간 측정
            print('book 활동 추천 시작')
            start = time.time()
            answer = self.llm(_input.to_messages())
            if answer.content.split('\n\t')[1].strip()[-1] != ',':
                print('에러발생------------------')
                answer.content = ','.join(answer.content.split('\n\t')).replace(',','', 1)

            print("answer type:", type(answer))
            print("answer:", answer)
            answer = self.output_parser.parse(answer.content)
            end = time.time()

            print(answer)
            print('book 활동 추천 완료')
            print(cb)
            print(end-start, '경과')
        return answer