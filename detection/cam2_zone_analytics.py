from ultralytics import YOLO
import supervision as sv
import cv2

from backend.event_service import save_event

VIDEO_PATH = "data/CAM2.mp4"

# -----------------
# MODEL
# -----------------

model = YOLO("yolov8n.pt")

tracker = sv.ByteTrack()

# -----------------
# VIDEO
# -----------------

cap = cv2.VideoCapture(VIDEO_PATH)

# -----------------
# ZONES
# -----------------

ZONES = {
    "CONSULTATION": (0, 250, 500, 1080),
    "SKINCARE": (500, 150, 1050, 1080),
    "MAKEUP": (1050, 100, 1920, 1080)
}

# Prevent duplicate zone events
visited = {}

# -----------------
# MAIN LOOP
# -----------------

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

    detections = detections[detections.class_id == 0]

    detections = tracker.update_with_detections(
        detections
    )

    # Draw Zones
    for zone_name, (x1, y1, x2, y2) in ZONES.items():

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            zone_name,
            (x1 + 10, y1 + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

    # Process tracked people
    for bbox, track_id in zip(
        detections.xyxy,
        detections.tracker_id
    ):

        if track_id is None:
            continue

        x1, y1, x2, y2 = bbox

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        # Check which zone the person is in
        for zone_name, (zx1, zy1, zx2, zy2) in ZONES.items():

            inside_zone = (
                zx1 <= center_x <= zx2
                and
                zy1 <= center_y <= zy2
            )

            if inside_zone:

                key = f"{track_id}_{zone_name}"

                if key not in visited:

                    visited[key] = True

                    save_event(
                        person_id=int(track_id),
                        event_type="ZONE_VISIT",
                        camera_id="CAM2",
                        zone=zone_name
                    )

                    print(
                        f"ZONE_VISIT -> ID {track_id} -> {zone_name}"
                    )

        # Draw person box
        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"ID {track_id}",
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "CAM2 Zone Analytics",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("Zone Analytics Completed")