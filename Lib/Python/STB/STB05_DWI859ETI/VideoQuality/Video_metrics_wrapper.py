import Video_metrics_robot  # this is your compiled .so file

def video_metrics(video_port, duration, trigger_id):
    return Video_metrics_robot.video_metrics(video_port, duration, trigger_id)
