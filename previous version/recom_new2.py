
import os
from langchain.llms import OpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.prompts.prompt import PromptTemplate
from langchain.cache import InMemoryCache

import time
 



class Act_Rec:
    """
    일반 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 chatGPT기반 활동 및 질문 추천
    도서 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 도서추천API 로직 이후 csv에서 뽑아온 도서요약 건 관련 질문 추천 
    """
    def __init__(self):
        self.llm = OpenAI(model_name='text-davinci-003', temperature=0.8, max_tokens=400)

    def general_recommend(self, major):
        """
        일반 관심분야 활동추천 기능
        major: 사용자의 입력값 - 관심분야
        """
        template = """{major}를 기반으로 아래의 정보를 출력해주세요. 예시 형식과 똑같이 작성합니다.
        - 탐구적인 에세이 주제 1개
        - 에세이 작성에 도움이 될만한 가이드 질문 3개
        - 아래와 완전히 똑같이 출력
        에세이 주제 : 내용
        Question1 내용
        Question2 내용
        Question3 내용 """
        prompt = PromptTemplate.from_template(template)
        with get_openai_callback() as cb:
            start = time.time()
            # llm 모델로 답변 작성
            answer = self.llm(prompt.format(major=major))
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
        template = """책의 요약글 {book_text}과 {major}를 연관지어 아래 정보를 출력해주세요.
        - 탐구적인 에세이 주제 1개
        - 에세이 작성에 도움이 될만한 가이드 질문 3개
        - 아래와 완전히 똑같이 출력 
        에세이 주제 : 내용 
        Question1 내용
        Question2 내용
        Question3 내용 """
        prompt = PromptTemplate.from_template(template)
        with get_openai_callback() as cb:
            start = time.time()
            # llm 모델로 답변 작성 
            answer = self.llm(prompt.format(major=major, book_text = book_text))
            end = time.time()
            print(answer)
            print('book 활동 추천 완료')
            print(cb)
            print(end-start, '경과')
        return answer
    
    


