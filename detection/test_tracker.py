import supervision as sv

tracker = sv.ByteTrack(
    track_activation_threshold=0.25,
    lost_track_buffer=60,
    minimum_matching_threshold=0.8,
    frame_rate=fps
)

print("ByteTrack Loaded Successfully")