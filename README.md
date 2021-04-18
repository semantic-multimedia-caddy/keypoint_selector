# Keypoint Selector

시맨틱 멀티미디어 키포인트 라벨링 툴. 일단 만들었지만, 이걸로 과연 regression 가능할까...

## Requirements
- Python 3.7 이상
- OpenCV (`conda install opencv`)

## Manual
기본적인 실행은,
```bash
python main.py --video VIDEO_PATH
```

프레임 간격 정해주기는,
```bash
python main.py --video VIDEO_PATH --interval 10 # 10 frame 간격으로 라벨링
```

숫자를 입력해서 라벨을 설정해준 후, 마우스 왼쪽클릭하면 해당 지점에 해당 라벨로 키포인트가 생성됨. 현재 내가 입력한 라벨이 뭔지는 터미널보면 나옴

- `0`~`9` 키포인트 라벨 설정. 십의자리 넘어가는 라벨의 경우, 그냥 연속으로 숫자 누르면됨
- `e` 누르면 종료
- `n` 누르면 다음 프레임
- `z` UNDO
