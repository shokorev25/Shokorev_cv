import cv2
import numpy as np

glasses_img = cv2.imread('dealwithit.png', cv2.IMREAD_UNCHANGED)

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]

        glasses_resized = cv2.resize(glasses_img, (w, int(glasses_img.shape[0] * (w / glasses_img.shape[1]))))

        glasses_height = glasses_resized.shape[0]
        glasses_width = glasses_resized.shape[1]

        for i in range(glasses_height):
            for j in range(glasses_width):
                if glasses_resized[i, j][3] != 0:  # Проверка, если пиксель не прозрачный
                    face_roi[i, j] = glasses_resized[i, j][:3]  # Наложение RGB компоненты

        frame[y:y+h, x:x+w] = face_roi

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
