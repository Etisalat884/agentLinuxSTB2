from robot.api.deco import keyword
from Video_metrics_robot import video_metrics

class VideoMetricsLibrary:

    @keyword("Run Video Metrics Multiple Times")
    def run_video_metrics_multiple_times(self, port="/dev/video0", duration=20, iterations=10):
        blocking_scores = []
        banding_scores = []

        for _ in range(iterations):
            blocking, banding = video_metrics(port, duration, iterations)
            blocking_scores.append(blocking)
            banding_scores.append(banding)

        avg_blocking = sum(blocking_scores) / len(blocking_scores) if blocking_scores else 0
        avg_banding = sum(banding_scores) / len(banding_scores) if banding_scores else 0

        return avg_blocking, avg_banding