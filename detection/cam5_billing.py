from ultralytics import YOLO
import supervision as sv
import cv2
from backend.event_service import save_event

VIDEO_PATH = "data/CAM5.mp4"

model = YOLO("yolov8s.pt")

tracker = sv.ByteTrack(
    lost_track_buffer=90
)

cap = cv2.VideoCapture(VIDEO_PATH)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# -------------------------
# BILLING ZONE
# -------------------------

ZONE_X1 = 700
ZONE_Y1 = 250

ZONE_X2 = 1700
ZONE_Y2 = 950

# -------------------------

counted_ids = set()

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

    cv2.rectangle(
        frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (255, 0, 0),
        3
    )

    for bbox, track_id in zip(
        detections.xyxy,
        detections.tracker_id
    ):

        x1, y1, x2, y2 = bbox

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        inside_zone = (
            ZONE_X1 <= center_x <= ZONE_X2
            and
            ZONE_Y1 <= center_y <= ZONE_Y2
        )

        if inside_zone:

            if track_id not in counted_ids:

                counted_ids.add(track_id)

                save_event(
                    person_id=int(track_id),
                    event_type="BILLING_VISIT",
                    camera_id="CAM5"
                )

                print(
                    f"BILLING VISIT -> {track_id}"
                )

        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"ID {track_id}",
            (int(x1), int(y1)-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

    cv2.putText(
        frame,
        f"Billing Visitors: {len(counted_ids)}",
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,0,0),
        2
    )

    cv2.imshow(
        "Billing Zone",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

print(
    f"Total Billing Visitors: {len(counted_ids)}"
)