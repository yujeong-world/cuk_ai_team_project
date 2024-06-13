# cuk_ai_team_project


## 가톨릭대학교 2024 1학기 인공지능 프로젝트
### 팀원 : 권유정. 정이령, 유승주, 오지민

###【Project 내용】
Wumpus World의 기초적인 형태를 구현해 본다. n 에이전트가 처한 환경
탐험하는 에이전트가 처한 환경은 4×4 격자로 구성되어 있으며, (1,1) 격자는 
안전하다(safe)고 가정한다. 4×4 격자 세계(Grid World)의 고정된 위치에 금
(gold), wumpus 괴물 및 웅덩이(pitch)가 존재한다. wumpus 괴물 및 웅덩이
가 발생할 확률은 각각의 격자에서 독립적이며, 0.10으로 가정한다. 에이전트
가 금을 획득하여 [1,1] 격자로 되돌아오면 탐험은 종료된다. 

### 에이전트의 센서를 통한 입력은 다음과 같다: 
[Stench, Breeze, Glitter, Bump, Scream] - Stench: wumpus 괴물의 존재 여부
- Breeze: 웅덩이의 존재 여부
- Glitter: 금(gold)의 존재 여부
- Bump: 벽(wall)의 존재 여부
- Scream: wumpus 괴물이 에이전트가 쏜 화살에 의하여 제거되었는지에 대
한 여부

### 개발 환경
- python
- 파이썬 라이브러리 : pygame

### 동작 구조
![image](https://github.com/yujeong-world/cuk_ai_team_project/assets/124220083/26810e21-a124-4342-82de-f51a9cb5af05)


### 실행 화면
![image](https://github.com/yujeong-world/cuk_ai_team_project/assets/124220083/6ca7cc1a-34b3-4a8d-8fe1-bc0d412a976b)


### 실행 방법
main.py 파일을 실행하면 작동합니다.
