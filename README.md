# 프로젝트 소개
2024_임베디드SW입문_라즈베리파이4_게임_프로젝트

## 프로젝트 명: Burger Time

### 프로젝트 소개
• 게임의 메인 아이템인 햄버거를 잘 만들어야 한다는 것을 강조하고 싶어서 게임 
	 이름에 버거(Burger)를 넣으려고 했고, 시간 안에 음식을 만들어야 하기 때문에, 
   타임(Time)을 이어 붙여서 게임에 대한 특징을 나타내고자 하였다.

### 선정이유
• 어렸을 때부터 가게를 관리하거나 음식을 만드는 타이쿤 같은 게임을 좋아했다. 
	 또한, 시간 안에 음식을 만들어 손님에게 대접해 주며 타임 어택을 하는 게임을 
   어렸을 때부터 자주 하였고, 즐겼다. 그렇게 내가 제일 좋아하는 게임을 실제로 
   직접 만들어 보고, 구현해 보고 싶어 햄버거 만들기 게임을 만들어 보게 되었다.

---

### 게임 방법

1. 게임 시작: 플레이어가 일하게 될 햄버거 가게의 이미지가 나타나며, 가게로
	           출근하는 이야기를 표현한다. 이 과정을 보여주며 게임이 시작된다.

2. 손님의 등장: 가게 내부의 공간으로 장소가 변한 후에, 일정 시간이 지나고 손님이
		      가게에 들어온다. 그 후에 들어온 손님은 말풍선을 통해 햄버거와 
 		      콜라 또는 감자튀김을 주문한다. 주문이 끝난 손님은 다시 돌아가고,
		      다른 손님이 다시 들어와 음식을 주문한다.

3. 주문 처리: 플레이어는 조이스틱과 버튼을 사용해서 올바른 재료들을 순서대로
		    쌓아서 햄버거(패티는 프라이팬에 5초 동안 구워야 함)를 만들거나,
 		    콜라 냉장고를 클릭해서 콜라를 꺼내거나, 감자를 튀김기로 7초 동안
		    튀겨서 감자튀김을 만드는 과정들을 통해 손님의 주문에 맞는 음식을
		    만들어야 한다. 이때 완성된 요리는 접시에 자동으로 각각 담긴다. 
		    마지막으로 손님의 주문에 맞는 요리를 다 만든 후에, 계산대 버튼을 
		    눌러야 손님에게 요리가 제공된다. (올바른 요리를 제공하면 엄지를 
		    위로 한 이미지를 사용자 옆에 출력하고, 올바르지 않은 요리를 
  	    제공하면 엄지를 아래로 한 이미지를 사용자 옆에 출력하여 나타낸다.)

4. 점수 계산: 제한 시간(15초) 안에 정확한 주문을 처리하면 왼쪽 아래에 주문 수가
		    늘어나게 되고, 총 10가지의 주문을 정확히 받으면 해피엔딩 이미지가
	 	    나오며 게임은 마무리된다. 만약, 주문을 정확히 처리하지 않고,
		    계산대 그림을 누르게 되면 오른쪽 아래의 하트가 사라지게 된다.
		    그렇게 3개의 하트가 모두 사라지게 되면 플레이어는 탈락하게 되고,
		    새드엔딩 이미지가 나오며 게임은 마무리된다.

5. 정지 및 재시작: 게임을 하던 도중 버튼을 통해 정지 및 재시작을 할 수 있다.

---

### 프로젝트 정보

- **개발 환경**: Raspberrypi4
- **사용 언어**: Python3

---
