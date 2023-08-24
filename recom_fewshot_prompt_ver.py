
import os
from langchain.agents import initialize_agent
from langchain.callbacks import get_openai_callback
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
import time
  
# API 키설정
OPENAI_API_KEY = "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"
#구글검색하려면 SERPAPI 필요(월 100회 무료/월 5000회 $50/월 15000회 $130/월 30000회 $250)
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


class cfg: 
    examples_book = [
    {
    "major":'동물학',
    "book_text":"'보아가 들려주는 원자 모형 이야기'는 덴마크의 물리학자 닐스 보어가 원자 모형의 역사와 원자의 구조에 대해 설명하는 책입니다. 이 책은 원자의 모형이 변해 가는 과정과, 그런 과정을 통해 인류가 알아낸 원자의 구조에 대한 설명은 물론 원자의 구조를 밝혀 낸 사람들의 이야기까지 자세히 들어 있습니다. 세상에서 가장 작은 세계에 대해 관심과 호기심이 많은 학생들과 일반인에게 적극 추천할 만한 책입니다.",
    "answer":"""{{'S1': '원자의 구조와 동물 생리학의 연결', 'Q1': '원자의 구조가 동물 생리학과 어떤 연관성이 있을까요? 원자의 구조가 동물의 기능과 동작에 어떤 영향을 미칠 수 있을까요?', 'Q2': '원자의 구조와 동물의 진화에 대한 이해는 어떻게 도움이 될 수 있을까요? 원자의 구조를 통해 동물의 진화적 특징을 분석하고 해석할 수 있는 방법은 무엇일까요?', 'Q3': '동물 생리학 연구에 있어 원자의 구조를 고려하는 것이 왜 중요한가요? 원자의 구조에 대한 이해가 동물의 신체 기능 및 행동을 이해하는 데 어떤 역할을 할 수 있을까요?'}}"""
    },
    {
    "major":"교육학",
    "book_text":"이케가야 유지의 『교양으로 읽는 뇌과학』은 뇌의 구조와 기능, 뇌과학이 밝혀낸 인간의 행동과 사고에 대한 다양한 주제를 다룬 교양서입니다. 이 책은 뇌과학의 최신 연구 결과를 바탕으로 뇌의 신비를 쉽고 재미있게 설명하고 있습니다. 또한, 뇌과학이 우리 삶에 어떻게 적용될 수 있는지에 대해 이야기하고 있습니다. 『교양으로 읽는 뇌과학』은 뇌에 대해 관심이 있는 사람이라면 누구나 쉽게 이해할 수 있는 책입니다.",
    "answer":"""{{"S1": "뇌과학의 중요성과 응용","Q1": "뇌과학이 교육학에 어떤 영향을 미칠 수 있을까요? 교육학 이론의 발전과정을 토대로 알아보세요","Q2": "뇌과학을 활용한 교육 방법에는 어떤 것들이 있나요? 교육학 이론 중 뇌과학분야와 접목시킨 이론이 있는지 찾아보세요!","Q3": "뇌과학적 관점에서 우리가 배울 수 있는 인간의 학습 능력에 대해 알려주세요. 미디어기술이 빠르게 발전하고 있는 우리 사회에서 이러한 학습능력을 키우기 위해서는 어떤 방법을 취해야할까요?"}}"""
    }]


    example_template_book = """
    관심분야:{major}
    책 내용:{book_text}
    AI:{answer}
    """
    example_prompt_book = PromptTemplate(
    input_variables=["major","book_text","answer"],
        template = example_template_book
    )

    examples_gen = [
    {"major":'건축학',
    "answer":"""{{"S1": "기존 건축물을 활용한 지속가능한 리모델링 방안 연구", "Q1": "기존 건축물의 재활용이 환경에 어떤 영향을 미칠까요? 건축물 재활용의 사례를 찾아 설명해보세요.", "Q2": "지속가능한 재료 및 에너지 사용을 통해 건축물의 효율성을 높이는 방법은 어떤 것이 있을까요? 최근 개발된 기술에 대해 찾아 사례로 들어보세요.","Q3": "기존 건축물을 보존하면서 건물의 기능을 향상시키는 방법은 어떤 것이 있나요? 해당 기술에 대해 연구한 사례를 찾아보세요!"}}"""
    },
    {"major":"교육학",
    "answer":"""{{"S1": "유아기 아동의 창의적 사고 발전을 위한 교육 방법","Q1": "유아기 아동의 창의적 사고를 어떻게 정의할 수 있을까요? 이 시기 아동의 창의력을 평가하는 방법이 있나요?","Q2": "유아기 아동의 창의적 사고 발전을 위해 어떤 교육 방법이 효과적일까요? 실제 교육 사례를 찾아보고 장단점을 파악해보세요!","Q3": "창의적 사고를 향상시키기 위한 교육 방법이 유아기 아동의 다른 발달 영역에 미치는 영향은 무엇일까요? 창의력 교육의 중요성에 대해 자세히 알아봅시다."}}"""
    }]

    example_template_gen = """
    관심분야:{major}
    AI:{answer}
    """
    example_prompt_gen = PromptTemplate(
    input_variables=["major","answer"],
        template = example_template_gen
    )



    response_schemas= [
        ResponseSchema(name="S1", description="추천된 주제"),
        ResponseSchema(name="Q1", description="첫번째 가이드 질문"),
        ResponseSchema(name="Q2", description="두번째 가이드 질문"),
        ResponseSchema(name="Q3", description="세번째 가이드 질문")
        ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    
    
    
class Act_Rec:
    """
    일반 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 chatGPT기반 활동 및 질문 추천
    도서 활동추천: 사용자의 입력(희망전공 또는 분야)에 따른 도서추천API 로직 이후 csv에서 뽑아온 도서요약 건 관련 질문 추천 
    """
    def __init__(self):
        self.llm = OpenAI(model_name='gpt-3.5-turbo', temperature=0.8, max_tokens=1500)
        self.response_schemas= cfg.response_schemas
        self.output_parser = cfg.output_parser
        self.format_instructions = cfg.format_instructions
        self.examples_book = cfg.examples_book
        self.example_prompt_book = cfg.example_prompt_book

        self.examples_gen = cfg.examples_gen
        self.example_prompt_gen = cfg.example_prompt_gen    


    def general_recommend(self, major):
        """
        일반 관심분야 활동추천 기능
        major: 사용자의 입력값 - 관심분야
        """
        
        task_description_gen = """
        관심 분야에 대한 창의적인 탐구 주제 1개를 추천해주세요. 주제에 대한 가이드 질문 3개를 길고 자세히 추천해주세요.\n{format_instructions}
        """

        instruction_gen = """
        관심분야: {major} 
        AI:"""

        few_shot_prompt_template = FewShotPromptTemplate(
        examples=self.examples_gen,
        example_prompt=self.example_prompt_gen,
        prefix=task_description_gen,
        suffix=instruction_gen,
        input_variables=["major",],
        partial_variables={'format_instructions':self.format_instructions},
        example_separator="\n\n"
        )


        _input = few_shot_prompt_template.format(major=major)                             # 유저 input값 입력
        with get_openai_callback() as cb:                                       # with 내 콜백 사항 answer 계산 제외 모두 삭제해도 됨
            print('일반 활동 추천 시작')
            # 시간 측정
            start = time.time()
            answer = self.llm(_input)
            print(answer)

            print("answer type:", type(answer))
            print("answer:", answer)
            answer = self.output_parser.parse(answer)
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

        task_description = """
        책 내용을 관심분야 {major}에 연결지어 독후감 또는 에세이작성을 위한 주제 1개를 추천해주세요. 주제에 대한 가이드 질문 3개를 길고 자세히 추천해주세요.\n{format_instructions} \n"""

        instruction = """
        관심분야: {major} 
        책 내용: {book_text}
        AI:"""

        few_shot_prompt_template = FewShotPromptTemplate(
        examples=self.examples_book,
        example_prompt=self.example_prompt_book,
        prefix=task_description,
        suffix=instruction,
        input_variables=["major","book_text"],
        partial_variables={'format_instructions':self.format_instructions},
        example_separator="\n\n"
        )
        _input = few_shot_prompt_template.format(major=major, book_text=book_text)         # 유저 input값(major) & 도서추천 결과 책요약(book_text) 입력
        with get_openai_callback() as cb:                                       # with 내 콜백 사항 answer 제외 모두 삭제해도 됨
            # 시간 측정
            print('book 활동 추천 시작')
            start = time.time()
            answer = self.llm(_input)
            print(answer)
            print("answer type:", type(answer))
            print("answer:", answer)
            answer = self.output_parser.parse(answer)
            end = time.time()

            print(answer)
            print('book 활동 추천 완료')
            print(cb)
            print(end-start, '경과')
        return answer
