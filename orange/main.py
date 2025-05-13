import cv2
import numpy as np
from ultralytics import YOLO
from skimage import draw

def load_orange_mask(path, hsv_lower, hsv_upper):
    image = cv2.imread(path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    mask = cv2.dilate(mask, np.ones((7, 7)))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    return image, (x, y, w, h)

def get_global_mask(masks, shape):
    if masks is None or len(masks) == 0:
        return np.zeros(shape[:2], dtype=np.float32)

    global_mask = masks.data.cpu().numpy()[0]
    for mask in masks.data.cpu().numpy()[1:]:
        global_mask += mask

    global_mask = cv2.resize(global_mask, (shape[1], shape[0])).astype(np.float32)

    rr, cc = draw.disk((5, 5), 5)
    struct = np.zeros((11, 11), np.uint8)
    struct[rr, cc] = 1
    return cv2.dilate(global_mask, struct, iterations=2)

def extract_and_resize_face(image, mask, target_shape):
    pos = np.where(mask > 0.5)
    if len(pos[0]) == 0:
        return None, None

    y1, y2 = int(np.min(pos[0])), int(np.max(pos[0]))
    x1, x2 = int(np.min(pos[1])), int(np.max(pos[1]))

    face = image[y1:y2, x1:x2]
    face_mask = mask[y1:y2, x1:x2]

    resized_face = cv2.resize(face, target_shape)
    resized_mask = cv2.resize(face_mask, target_shape).astype(np.float32)
    resized_mask = (resized_mask > 0.5).astype(np.uint8) * 255

    return resized_face, resized_mask

def overlay_face(base, face, mask, position):
    x, y, w, h = position
    roi = base[y:y + h, x:x + w]

    if roi.shape != face.shape or roi.size == 0:
        return base

    bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
    fg = cv2.bitwise_and(face, face, mask=mask)
    combined = cv2.add(bg, fg)
    base[y:y + h, x:x + w] = combined
    return base

def main():
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

    model = YOLO("facial_best.pt")
    orange_template, orange_bbox = load_orange_mask("oranges.png", 
                                                     hsv_lower=np.array((10, 240, 200)),
                                                     hsv_upper=np.array((15, 255, 255)))
    x, y, w, h = orange_bbox

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting ...")
            break

        oranges = orange_template.copy()
        result = model(frame)[0]
        global_mask = get_global_mask(result.masks, frame.shape)

        face, face_mask = extract_and_resize_face(frame, global_mask, (w, h))
        if face is not None:
            oranges = overlay_face(oranges, face, face_mask, (x, y, w, h))
        else:
            print("No face detected.")

        cv2.imshow("Image", oranges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
