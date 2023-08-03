
import os
from langchain.llms import OpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
import time

# API 키설정
OPENAI_API_KEY = "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"
#구글검색하려면 SERPAPI 필요(월 100회 무료/월 5000회 $50/월 15000회 $130/월 30000회 $250)
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

 
class Act_Rec:
    """
    일반 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 chatGPT기반 활동 및 질문 추천
    도서 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 도서추천API 로직 이후 csv에서 뽑아온 도서요약 건 관련 질문 추천 
    """
    def __init__(self):
        self.llm = OpenAI(model_name='text-davinci-003', temperature=0.8, max_tokens=1000)


    def general_recommend(self, major):
        """
        일반 관심분야 활동추천 기능
        major: 사용자의 입력값 - 관심분야
        """
        template = """당신은 고등학생의 관심사를 기반으로 탐구적인 에세이 주제 1 개, 에세이 작성에 도움이 될만한 가이드 질문 3개를 추천해주는 전문 AI입니다. 나의 관심사는 {major}입니다.
        아래 예시처럼 $s0, $q0~3을 반드시 꼭 넣고, 글머리 형식을 반드시 유지해줘.
        
        $s0 에세이 주제 :

        $q1 질문 1.
        $q2 질문 2.
        $q3 질문 3. """
        prompt = PromptTemplate.from_template(template)
        start = time.time()
        # llm 모델로 답변 작성
        answer = self.llm(prompt.format(major=major))
        end = time.time()
        print(answer)
        print('일반 활동 추천 완료')
        print(end-start, '경과\n---------------------------------------------------')
        return answer

    def book_recommend(self, major, book_text):
        """
        도서 활동추천 기능
        major: 사용자의 입력값 - 관심분야
        book_text: 사용자의 입력값에 따라 추천 API를 돌고 나온 추천 도서의 내용 요약 정보
        """
        template = """책의 요약글 {book_text}을 읽고 글의 내용과 연관하여, 학생들이 작성할 수 있는 에세이 주제 1개와 그 글을 쉽게 쓸 수 있게 도와주는 가이드 질문 3개를 제공해줘. 관심사는 : {major}
        아래 예시처럼 $s0, $q0~3을 반드시 꼭 넣고, 글머리 형식을 반드시 유지해줘.
        
        $s0 에세이 주제 :
        
        $q1 질문 1.
        $q2 질문 2.
        $q3 질문 3. """
        prompt = PromptTemplate.from_template(template)
        start = time.time()
        # llm 모델로 답변 작성 
        answer = self.llm(prompt.format(major=major, book_text = book_text))
        end = time.time()
        print(answer)
        print('book 활동 추천 완료')
        print(end-start, '경과')
        return answer
    


