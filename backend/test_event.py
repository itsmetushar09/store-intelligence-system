from backend.event_service import save_event

save_event(
    person_id=1,
    event_type="ENTRY",
    camera_id="CAM3"
)

save_event(
    person_id=1,
    event_type="EXIT",
    camera_id="CAM3"
)

print("Test Complete")