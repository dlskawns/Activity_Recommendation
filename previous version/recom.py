
import os
from langchain.llms import OpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
import time

# API 키설정
OPENAI_API_KEY = "api_key"
#구글검색하려면 SERPAPI 필요(월 100회 무료/월 5000회 $50/월 15000회 $130/월 30000회 $250)
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
  
# 예시 넣기
class cfg:
    examples_book = [
  { "major": "기계공학",
   "book_text": "생각하는 뇌, 생각하는 기계는 제프 호킨스와 샌드라 블레이크슬리가 공동으로 저술한 책으로, 뇌와 인공지능에 대한 고찰을 담고 있습니다. 이 책은 뇌가 어떻게 작동하는지,\
      그리고 그 지식을 바탕으로 어떻게 인공지능을 만들 수 있는지를 탐구합니다. 저자들은 뇌는 신경망으로 이루어져 있으며, 이 신경망은 서로 연결되어 복잡한 기능을 수행한다고 주장합니다. \
        또한, 인공지능은 뇌의 신경망과 유사한 구조를 가질 경우 인간과 같은 지능을 가질 수 있다고 주장합니다. 이 책은 뇌와 인공지능에 대한 이해를 높이고, 미래의 인공지능이 어떻게 발전할 것인지에 대한 통찰력을 제공합니다.",
   "answer":
"""
$s0 에세이 주제: 인간과 기계공학의 상호작용

$q0 가이드 질문:
$q1 1. 기계공학은 어떻게 인간의 삶을 향상시키고 있을까요?
$q2 2. 인간과 기계공학의 협력은 어떤 도전과제를 가지고 있을까요?
$q3 3. 인공지능과 로봇공학이 발전함에 따라 인간의 역할은 어떻게 변할까요?
"""},
  {'major': '경찰행정학',
   'book_text': "케네스 미노그의 '정치란 무엇인가'는 정치의 본질과 역사를 다룬 책입니다. 저자는 정치는 권력과 질서를 둘러싼 갈등이며, 이 갈등은 언어와 폭력의 두 가지 수단을 통해 해결된다고 주장합니다. \
    또한, 저자는 정치는 고대 그리스와 로마에서 시작된 서구의 전통이며, 이 전통은 근대 국가의 형성과 민주주의의 발전으로 이어졌다고 설명합니다. 마지막으로, 저자는 정치의 미래에 대해 낙관적인 전망을 제시하며, \
        정치가 인류의 삶을 개선하는 데 중요한 역할을 할 것이라고 주장합니다.",
   'answer':
"""
$s0 에세이 주제: 경찰행정학의 중요성과 도전

$q0 가이드 질문:
$q1 1. 경찰행정학은 무엇이며, 왜 중요한가요?
$q2 2. 경찰의 역할과 책임은 무엇이며, 어떤 도전과 과제들이 있는가요?
$q3 3. 경찰행정학을 통해 어떻게 더 효과적인 경찰 조직을 구축할 수 있을까요?
"""}]
    examples_act = [{"interested": "신소재화합물",
    "answer":
"""
$s0 에세이 주제: 신소재화합물의 가능성

$q0 에세이 작성에 도움이 될 질문:
$q1 1. 신소재화합물이 지구감시 사업에 어떻게 도움을 주었나요?
$q2 2. 신소재화합물을 이용한 응용프로그램에 대해 당신이 어떤 생각을 가지고 있나요?
$q3 3. 이러한 기술이 사회개발에 어떤 영향을 미치고 있나요?
"""}]


class Act_Rec:
    """
    일반 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 chatGPT기반 활동 및 질문 추천
    도서 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 도서추천API 로직 이후 csv에서 뽑아온 도서요약 건 관련 질문 추천 
    """
    def __init__(self, cfg):
        # super(Act_Rec, self).__init__()
        self.examples_book = cfg.examples_book
        self.examples_act = cfg.examples_act
        self.llm = OpenAI(model_name='text-davinci-003', temperature=0.8, max_tokens=1000)


    def general_recommend(self, major):
        """
        일반 관심분야 활동추천 기능
        major: 사용자의 입력값 - 관심분야
        """

        # Few shot 진행을 위한 예시 prompt 생성
        example_prompt = PromptTemplate(input_variables=["interested", "answer"], template="관심사: {interested}\n{answer}")
        start = time.time()
        print('일반 활동 추천 진행')
        # Few shot으로 GPT 활용 진행
        prompt = FewShotPromptTemplate(
        examples=self.examples_act,
        example_prompt=example_prompt,
        prefix = """당신은 고등학생의 관심사를 기반으로 중복되지 않는 에세이 주제 1 개, 에세이 작성에 도움이 될만한 가이드 질문 3개를 추천해주는 전문 AI입니다. 나의 관심사는 {interested}입니다.""",
        suffix="관심사: {interested}",
        input_variables=["interested"])

        # llm 모델로 답변 작성
        answer = self.llm(prompt.format(interested=major))
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
        # Few shot 진행을 위한 예시 prompt 생성
        example_prompt = PromptTemplate(input_variables=["major", "book_text", "answer"], template="Question: {major}\n{book_text}\n{answer}")
        start = time.time()
        print('book 활동 추천 진행')
        # Few shot으로 GPT 활용 진행
        prompt = FewShotPromptTemplate(
        examples=self.examples_book,
        example_prompt=example_prompt,
        prefix = """책의 요약글을 읽고 글의 내용과 연관하여, 학생들이 작성할 수 있는 에세이 주제 1개와 그 글을 쉽게 쓸 수 있게 도와주는 가이드 질문 3개를 제공해줘. 책 요약은 출력하지마.
        관심사: {major}, 책요약: {book_text} """,
        suffix="관심사: {major}",
        input_variables=["major", "book_text"])
        

        # llm 모델로 답변 작성 
        answer = self.llm(prompt.format(major=major, book_text = book_text))
        end = time.time()
        print(answer)
        print('book 활동 추천 완료')
        print(end-start, '경과')
        return answer
    


