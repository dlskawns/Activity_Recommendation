# Activity_Recommendation
마이폴리오 활동 추천패키지 

### 사용방법

0. 경로 초기화를 한다.
```
cd 
```

2. 폴더를 생성한다.
```
mkdir 폴더명
```
2. 폴더에 들어간다. 반드시 해당 폴더 명이 아래와 같이 있는지 확인 할것 
```
cd 폴더명
```
3. git 클론 진행 - 테스트용 브랜치로 가져온다

```
git clone -b branch prompt/quality_control https://github.com/dlskawns/Activity_Recommendation.git
```

4. conda 가상환경 확인하기
```
conda env list
```

4-1. 가상환경 없을 경우 만들기
```
conda create -n 가상환경이름 python=3.8

중간에 y 입력
```

5. 특정 가상환경을 확인했으면 가상환경 실행 -> 왼쪽의 (base)가 (가상환경명)으로 바뀐것 확인할 것
```
conda activate 가상환경 이름
```

6. 패키지 설치
```
pip install -r requirements.txt
```

7. vscode 상에서 recom_new3_1.py 파일의 openai key 부분 수정, 저장
```
터미널로 할 경우, 해당 디렉토리에서 
1. vi recom_new3_1.py 입력

2. i키를 누르면 파일 내용 수정 가능

3. openai key 입력 부분 'sk-쏼라쏼라'입력 후 esc키 누르기

4. 이후 :wq 입력하여 파일 수정 완료
```

8. 실행
```
python main.py

7000번(도서 번호) 내로 입력 시 파일 실행됨
```

9. 프롬프트 변경 원할 경우, recom_new3_1.py 파일에서 변경, 저장을 꼭 한 뒤에 실행할 것. 
