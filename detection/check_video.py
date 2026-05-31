import cv2

video_path = "data/CAM2.mp4"

cap = cv2.VideoCapture(video_path)

print("Opened:", cap.isOpened())
print("Width:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Height:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("FPS:", cap.get(cv2.CAP_PROP_FPS))

ret, frame = cap.read()

print("First Frame Read:", ret)

cap.release()