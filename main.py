
from recom_fewshot_prompt_ver import Act_Rec
import os
import time 
import pandas as pd
import langchain
from langchain.cache import InMemoryCache


def main(input_value):
    """
    추천 API 결과 값을 통해 처리
    input_value: 추천된 책 no.
    """
    
    # 도서 데이터셋 경로 설정
    data_path = 'MF_BookDB.ver4.63.csv'
    book_data = pd.read_csv(data_path)
    
    # 추천 API 직후 추천된 도서에 따른 정보 가져오기
    major = book_data['중분류'][input_value]            # 관련분야(학과)
    book_text = book_data['Bard 책 요약'][input_value]  # 책 내용 요약
    print(major)
    print(book_text)
    # 활동 추천 인스턴스 생성
    book_act_rec = Act_Rec()

    # 일반활동 추천
    general_act = book_act_rec.general_recommend(major)
    # 도서활동 추천
    book_act = book_act_rec.book_recommend(major, book_text)

    return general_act, book_act


if __name__ == '__main__':
    
    start = time.time()
    main(int(input()))
    end = time.time()
    print(f'{end-start:.5f}초 소요') 