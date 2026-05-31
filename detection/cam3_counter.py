import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
from ultralytics import YOLO
import supervision as sv
import cv2
from backend.event_service import save_event

VIDEO_PATH = "data/CAM3.mp4"

# ------------------------
# MODEL
# ------------------------

model = YOLO("yolov8s.pt")

tracker = sv.ByteTrack(
    lost_track_buffer=90
)

# ------------------------
# VIDEO
# ------------------------

cap = cv2.VideoCapture(VIDEO_PATH)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# ------------------------
# DOOR REGION
# ------------------------

DOOR_X1 = 1050
DOOR_X2 = 1920

LINE_Y = 280

# ------------------------
# COUNTERS
# ------------------------

entered_ids = set()
exited_ids = set()

track_history = {}

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

    detections = tracker.update_with_detections(detections)

    # ------------------------
    # DRAW ENTRY LINE
    # ------------------------

    cv2.line(
        frame,
        (DOOR_X1, LINE_Y),
        (DOOR_X2, LINE_Y),
        (0, 0, 255),
        4
    )

    # ------------------------
    # DRAW DOOR REGION
    # ------------------------

    cv2.rectangle(
        frame,
        (DOOR_X1, 0),
        (DOOR_X2, height),
        (255, 0, 0),
        2
    )

    for bbox, track_id in zip(
        detections.xyxy,
        detections.tracker_id
    ):

        x1, y1, x2, y2 = bbox

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        # ------------------------
        # IGNORE PEOPLE OUTSIDE DOOR AREA
        # ------------------------

        if center_x < DOOR_X1 or center_x > DOOR_X2:
            continue

        # ------------------------
        # TRACK HISTORY
        # ------------------------
        if track_id not in track_history:
            track_history[track_id] = center_y

        previous_y = track_history[track_id]

        # ------------------------
        # ENTRY / EXIT
        # ------------------------
        if (
            previous_y < LINE_Y
            and center_y > LINE_Y
            and track_id not in entered_ids
        ):
            entered_ids.add(track_id)
            save_event(
                person_id=int(track_id),
                event_type="ENTRY",
                camera_id="CAM3"
            )
            print(f"ENTRY : {track_id}")

        elif (
            previous_y > LINE_Y
            and center_y < LINE_Y
            and track_id not in exited_ids
        ):
            exited_ids.add(track_id)
            save_event(
                person_id=int(track_id),
                event_type="EXIT",
                camera_id="CAM3"
            )
            print(f"EXIT : {track_id}")

        # update history
        track_history[track_id] = center_y

        # ------------------------
        # DRAW BOX
        # ------------------------
        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 255, 0),
            2
        )

        cv2.circle(
            frame,
            (center_x, center_y),
            5,
            (0, 255, 255),
            -1
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

    # ------------------------
    # DISPLAY COUNTS
    # ------------------------
    cv2.putText(
        frame,
        f"Entries: {len(entered_ids)}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Exits: {len(exited_ids)}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow("Counter", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("\nFINAL RESULTS")
print("Entries:", len(entered_ids))
print("Exits:", len(exited_ids))