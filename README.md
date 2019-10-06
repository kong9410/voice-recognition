# voice_recognition
음성인식을 통한 회의 내용 기록 프로그램

팀 명 : 담아전구  
팀 장 : 공민철  
팀 원 : 고민재, 박경민

## 구글 Cloud 음성인식 API

https://webnautes.tistory.com/1247 참조

## 실행법

1. 아나콘다3 파이썬이 설치되어 있어야합니다.

2. `conda env create -f environment.yml` 명령어로 가상환경을 설치합니다

3. `conda activate voiceenv` 명령어로 가상환경을 실행시킵니다.

4. 음성인식을 구동시키려면 개인 컴퓨터에 구글 음성인식 api가 설치되어 있어야합니다.

5. 음성분석을 하기 위해서는 uploadproject 폴더로 들어가 `python manage.py runserver` 명령어를 실행하면 됩니다.

6. 웹 페이지 접속 기본 url은 localhost:8000 입니다. 이는 실행하는 사람의 환경에 따라 다를 수도 있습니다.

