from ultralytics import YOLO
import supervision as sv
import cv2
import torch

print("CUDA Available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
# Load model
model = YOLO("yolov8n.pt")

if torch.cuda.is_available():
    model.to("cuda")

# Tracker
tracker = sv.ByteTrack()

# Video
video_path = "data/CAM2.mp4"

cap = cv2.VideoCapture(video_path)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

out = cv2.VideoWriter(
    "data/output_tracking.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

frame_no = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(
    frame,
    conf=0.4,
    verbose=False
)[0]

    detections = sv.Detections.from_ultralytics(results)

    detections = detections[detections.confidence > 0.4]

    detections = detections[detections.class_id == 0]

    detections = tracker.update_with_detections(detections)

    for bbox, track_id in zip(
        detections.xyxy,
        detections.tracker_id
    ):

        x1, y1, x2, y2 = map(int, bbox)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"ID {track_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

    out.write(frame)

    frame_no += 1

    if frame_no % 50 == 0:
        print(f"Processed {frame_no} frames")

cap.release()
out.release()

print("Tracking complete")