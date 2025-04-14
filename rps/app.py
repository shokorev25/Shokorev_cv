import ultralytics
from ultralytics import YOLO
import numpy as np
from pathlib import Path
import cv2
import time

path = Path(__file__).parent
model_path = path / "facial_best.pt"
model = YOLO(model_path)

cap = cv2.VideoCapture(0)
image = cv2.imread("scirock.jpg")

state = "idle"  # wait, result
prev_time = 0
cur_time = 0
player_1_hand = ""
player_2_hand = ""
game_result = ""
timer = 5

def find_winner():
    if player_1_hand == player_2_hand:
        game_res = "draw"
    elif player_1_hand == "rock" and player_2_hand == "scissors":
        game_res = "player_1_won"
    elif player_1_hand == "rock" and player_2_hand == "paper":
        game_res = "player_2_won"
    elif player_1_hand == "paper" and player_2_hand == "scissors":
        game_res = "player_2_won"
    elif player_1_hand == "paper" and player_2_hand == "rock":
        game_res = "player_1_won"
    elif player_1_hand == "scissors" and player_2_hand == "rock":
        game_res = "player_2_won"
    elif player_1_hand == "scissors" and player_2_hand == "paper":
        game_res = "player_1_won"
    else:
        game_res = "idk"
    return game_res

while cap.isOpened():
    ret, frame = cap.read()
    cv2.putText(frame, f"{state} - {5 - timer}", (20, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # frame = image
    # cv2.imshow("Camera", frame)
    results = model(frame)
    result = results[0]

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

    if not result:
        continue
    print(len(result.boxes.xyxy))
    # anno_frame = results[0].plot()

    if len(result.boxes.xyxy) == 2:
        labels = []
        for ind, xyxy in enumerate(result.boxes.xyxy):
            x1, y1, x2, y2 = xyxy.numpy().astype("int")
            print(result.boxes.cls)
            print(result.names)
            label = result.names[result.boxes.cls[ind].item()].lower()
            labels.append(label)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
            cv2.putText(frame, f"{labels[-1]}", (x1 + 20, y1 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        player_1_hand, player_2_hand = labels
        if player_1_hand == "rock" and player_2_hand == "rock" and state == "idle":
            state = "wait"
            prev_time = time.time()
        if state == "result":
            cv2.putText(frame, f"{game_result}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if state == "wait":
        timer = round(time.time() - prev_time, 1)
    if timer >= 5:
        timer = 5
        if state == "wait":
            state = "result"
            game_result = find_winner()
        elif state == "result":
            state = "wait"
    if state == "result":
        timer = round(time.time() - prev_time, 1)

    cv2.imshow("YOLO", frame)

    # cv2.imshow("YOLO", frame)

# cv2.namedWindow("YOLO", cv2.WINDOW_NORMAL)

cap.release()
cv2.destroyAllWindows()
