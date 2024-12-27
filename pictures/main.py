import cv2
import numpy as np

video_path = "output.avi"
output_file = "videva.txt"
threshold = 0.1  
min_area = 5000   
max_area = 50000  

reference = np.zeros((500, 500), dtype=np.uint8)
cv2.rectangle(reference, (150, 250), (350, 450), 255, -1)
cv2.fillPoly(reference, [np.array([[150, 250], [250, 100], [350, 250]], dtype=np.int32)], 255)
ref_contour, _ = cv2.findContours(reference, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
ref_contour = ref_contour[0]

video = cv2.VideoCapture(video_path)
match_count, frame_count = 0, 0

while True:
    ret, frame = video.read()
    if not ret:
        break
    frame_count += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  
    _, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) < 7: 
                continue
            
            match = cv2.matchShapes(contour, ref_contour, cv2.CONTOURS_MATCH_I1, 0.0)
            if match < threshold:
                match_count += 1
                break  

video.release()

with open(output_file, "w") as f:
    f.write(f"Total frames: {frame_count}\n")
    f.write(f"Matching frames: {match_count}\n")

print(f"Готово. Total frames: {frame_count}, Matching frames: {match_count}")
