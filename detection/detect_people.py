import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8s.pt")

# Input video
video_path = "data/CAM2.mp4"

cap = cv2.VideoCapture(video_path)

# Video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Output video
out = cv2.VideoWriter(
    "data/output_detection.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, verbose=False)

    for result in results:
        for box in result.boxes:

            cls = int(box.cls[0])

            # Person class = 0
            if cls == 0:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                confidence = float(box.conf[0])

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Person {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0,255,0),
                    2
                )

    out.write(frame)

    frame_count += 1

    if frame_count % 50 == 0:
        print(f"Processed {frame_count} frames")

cap.release()
out.release()

print("Detection Complete")
print("Saved: data/output_detection.mp4")