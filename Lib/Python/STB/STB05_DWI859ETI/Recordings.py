# import os
# import glob
# import xml.etree.ElementTree as ET
# from datetime import datetime
# import subprocess
# import shutil 


# class VideoLogOverlay:
#     def __init__(self, font_path=None):
#         self.font_path = font_path or "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
#         self.recording_start = None
#         self.recording_stop = None
#         self.logs = []
#         self.latest_xml = None
#         self.input_video = None
#         self.output_video = None
#         self.xml_dir = None
#         self.video_dir = None
#         self.output_dir = None

#     @staticmethod
#     def parse_time(s):
#         return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")

#     def get_latest_xml(self):
#         xml_files = glob.glob(os.path.join(self.xml_dir, "*.xml"))
#         if not xml_files:
#             raise FileNotFoundError("No XML files found.")
#         self.latest_xml = max(xml_files, key=os.path.getmtime)
#         return self.latest_xml

#     def parse_xml(self):
#         if not self.latest_xml:
#             raise ValueError("Latest XML file is not set. Run get_latest_xml() first.")

#         tree = ET.parse(self.latest_xml)
#         root = tree.getroot()

#         for kw in root.iter('kw'):
#             if kw.attrib.get('name') == 'Start Process':
#                 self.recording_start = self.parse_time(kw.find('status').attrib['start'])
#             elif kw.attrib.get('name') == 'Stop STB Screen Recording for both pass and fail':
#                 for inner_kw in kw.iter('kw'):
#                     if inner_kw.attrib.get('name') == 'Terminate Process':
#                         self.recording_stop = self.parse_time(inner_kw.find('status').attrib['start'])
#             if self.recording_start and self.recording_stop:
#                 break

#         if not self.recording_start or not self.recording_stop:
#             raise ValueError("Start or Stop time not found in XML.")

#     # def collect_logs(self):
#     #     if not self.latest_xml:
#     #         raise ValueError("Latest XML file is not set. Run get_latest_xml() first.")

#     #     tree = ET.parse(self.latest_xml)
#     #     root = tree.getroot()

#     #     self.logs = []
#     #     for kw in root.iter('kw'):
#     #         if kw.attrib.get('name') == 'Log To Console':
#     #             arg = kw.find('arg')
#     #             status = kw.find('status')
#     #             if arg is not None and status is not None:
#     #                 log_time = self.parse_time(status.attrib['start'])
#     #                 if self.recording_start <= log_time <= self.recording_stop:
#     #                     self.logs.append((log_time - self.recording_start, arg.text.strip()))

#     #     if not self.logs:
#     #         raise ValueError("No logs found between start and stop time.")

#     def collect_logs(self):
#         if not self.latest_xml:
#             raise ValueError("Latest XML file is not set. Run get_latest_xml() first.")

#         tree = ET.parse(self.latest_xml)
#         root = tree.getroot()

#         self.logs = []
#         for kw in root.iter('kw'):
#             if kw.attrib.get('name') == 'Log To Console':
#                 arg = kw.find('arg')
#                 status = kw.find('status')
#                 if arg is not None and status is not None:
#                     log_time = self.parse_time(status.attrib['start'])
#                     if self.recording_start <= log_time <= self.recording_stop:
#                         self.logs.append((log_time - self.recording_start, arg.text.strip()))

#         return len(self.logs) > 0

#     def get_latest_video(self):
#         video_files = glob.glob(os.path.join(self.video_dir, "*.mp4"))
#         if not video_files:
#             raise FileNotFoundError("No video files found in recordings directory.")
#         self.input_video = max(video_files, key=os.path.getmtime)
#         return self.input_video

#     def create_drawtext_filters(self):
#         if not self.logs:
#             raise ValueError("No logs collected. Run collect_logs() first.")

#         drawtext_filters = []

#         for log_time, message in self.logs:
#             start_sec = log_time.total_seconds()
#             end_sec = start_sec + 2
#             safe_message = message.replace(":", r'\:').replace("'", r"\'")
#             drawtext = (
#                 f"drawtext=fontfile='{self.font_path}':"
#                 f"text='{safe_message}':"
#                 f"enable='between(t,{start_sec:.2f},{end_sec:.2f})':"
#                 f"x=(w-text_w)/2:y=h-th-40:fontsize=35:fontcolor=white:"
#                 f"box=1:boxcolor=black@0.5"
#             )
#             drawtext_filters.append(drawtext)

#         # Add timestamp overlay
#         timestamp_filter = (
#             f"drawtext=fontfile='{self.font_path}':"
#             f"text='%{{pts\\:hms}}':x=10:y=10:fontsize=20:fontcolor=white:"
#             f"box=1:boxcolor=black@0.5"
#         )
#         drawtext_filters.append(timestamp_filter)

#         return ",".join(drawtext_filters)

#     def generate_output_path(self):
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         self.output_video = os.path.join(self.output_dir, f"output_{timestamp}.mp4")
#         return self.output_video

#     def run_ffmpeg(self):
#         if not self.input_video:
#             raise ValueError("Input video is not set. Run get_latest_video() first.")
#         filter_str = self.create_drawtext_filters()
#         self.generate_output_path()

#         subprocess.run([
#             'ffmpeg',
#             '-i', self.input_video,
#             '-vf', filter_str,
#             '-c:a', 'copy',
#             self.output_video
#         ], check=True)

#         print(f"✅ Video with embedded subtitles created: {self.output_video}")



#     # def run(self):
#     #     # Set the directories
#     #     self.xml_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/STB05_DWI859ETI/Report"
#     #     self.video_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/STB05_DWI859ETI"

#     #     # Set the new output directory
#     #     self.output_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/STB05_DWI859ETI/OutputRecordings"

#     #     # Ensure the output directory exists
#     #     os.makedirs(self.output_dir, exist_ok=True)

#     #     print("🔍 Getting latest XML file...")
#     #     self.get_latest_xml()
#     #     print(f"📄 Latest XML: {self.latest_xml}")

#     #     print("⏳ Parsing XML for recording times...")
#     #     self.parse_xml()
#     #     print(f"Start: {self.recording_start}, Stop: {self.recording_stop}")

#     #     print("📝 Collecting logs between start and stop times...")
#     #     self.collect_logs()
#     #     print(f"Collected {len(self.logs)} logs.")

#     #     print("🎥 Finding latest video file...")
#     #     self.get_latest_video()
#     #     print(f"Latest video: {self.input_video}")

#     #     print("▶️ Running FFmpeg to embed captions...")
#     #     self.run_ffmpeg()


#     def run(self):
#         # Set the directories
#         self.xml_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/STB05_DWI859ETI/Report"
#         self.video_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/STB05_DWI859ETI"
#         self.output_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/STB05_DWI859ETI/OutputRecordings"
#         os.makedirs(self.output_dir, exist_ok=True)

#         print("🔍 Getting latest XML file...")
#         self.get_latest_xml()
#         print(f"📄 Latest XML: {self.latest_xml}")

#         print("⏳ Parsing XML for recording times...")
#         self.parse_xml()
#         print(f"Start: {self.recording_start}, Stop: {self.recording_stop}")

#         print("📝 Collecting logs between start and stop times...")
#         logs_found = self.collect_logs()

#         print("🎥 Finding latest video file...")
#         self.get_latest_video()
#         print(f"Latest video: {self.input_video}")

#         if logs_found:
#             print("▶️ Running FFmpeg to embed captions...")
#             self.run_ffmpeg()
#         else:
#             print("⚠️ No logs found. Copying original video to output...")
#             self.generate_output_path()
#             shutil.copy(self.input_video, self.output_video)
#             print(f"✅ Original video copied to: {self.output_video}")

# # Example usage:
# if __name__ == "__main__":
#     overlay = VideoLogOverlay()
#     overlay.run()

import os
import glob
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import subprocess
import platform


class VideoLogOverlay:
    def __init__(self, font_path=None):
        # Use Arial on Windows, DejaVu on *nix
        if font_path:
            self.font_path = font_path
        else:
            self.font_path = (
                r"C:\Windows\Fonts\arial.ttf"
                if platform.system() == 'Windows'
                else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            )

        self.recording_start = None
        self.recording_stop = None
        self.logs = []
        self.testcases = []
        self.latest_xml = None
        self.input_video = None
        self.output_video = None
        self.xml_dir = None
        self.video_dir = None
        self.output_dir = None

    @staticmethod
    def parse_time(ts_str, fmt=None):
        """Parse ISO or Robot's YYYYMMDD style timestamp."""
        if not ts_str:
            return None
        if fmt:
            return datetime.strptime(ts_str, fmt)
        try:
            return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            return datetime.strptime(ts_str, "%Y%m%d %H:%M:%S.%f")

    def get_latest_xml(self):
        xmls = glob.glob(os.path.join(self.xml_dir, "*.xml"))
        if not xmls:
            raise FileNotFoundError(f"No XML files in {self.xml_dir}")
        self.latest_xml = max(xmls, key=os.path.getmtime)
        return self.latest_xml

    def parse_xml(self):
        tree = ET.parse(self.latest_xml)
        root = tree.getroot()
        for kw in root.iter('kw'):
            nm = kw.attrib.get('name', '')
            if nm == 'Start Process':
                self.recording_start = self.parse_time(
                    kw.find('status').attrib.get('start')
                )
            elif nm == 'Terminate Process':
                self.recording_stop = self.parse_time(
                    kw.find('status').attrib.get('start')
                )
            if self.recording_start and self.recording_stop:
                break
        if not (self.recording_start and self.recording_stop):
            raise ValueError("Could not find recording start/stop in XML.")

    def parse_testcases(self):
        """
        Extract each <test>…<status start=… elapsed=…> and compute both start & end.
        """
        tree = ET.parse(self.latest_xml)
        root = tree.getroot()

        # strip namespace if present
        ns = ''
        if root.tag.startswith('{'):
            ns = root.tag.split('}')[0] + '}'

        for test in root.findall(f'.//{ns}test'):
            name = test.attrib.get('name')
            status = test.find(f'{ns}status')
            if not (name and status is not None):
                continue

            start_s = status.attrib.get('start')
            elapsed = status.attrib.get('elapsed')
            end_s = status.attrib.get('endtime') or status.attrib.get('end')

            # parse start
            fmt = "%Y%m%d %H:%M:%S.%f" if ' ' in start_s else "%Y-%m-%dT%H:%M:%S.%f"
            dt_start = self.parse_time(start_s, fmt)

            # parse or compute end
            if end_s:
                dt_end = self.parse_time(end_s, fmt)
            elif elapsed:
                dt_end = dt_start + timedelta(seconds=float(elapsed))
            else:
                print(f"[WARN] no end or elapsed for '{name}', skipping")
                continue

            off_start = (dt_start - self.recording_start).total_seconds()
            off_end = (dt_end - self.recording_start).total_seconds()
            self.testcases.append((off_start, off_end, name))

        if not self.testcases:
            raise ValueError("No valid <test> entries found in XML.")

    def collect_logs(self):
        tree = ET.parse(self.latest_xml)
        root = tree.getroot()
        for kw in root.iter('kw'):
            if kw.attrib.get('name') == 'Log To Console':
                arg = kw.find('arg')
                status = kw.find('status')
                if arg is not None and status is not None and arg.text is not None:
                    ts = status.attrib.get('start')
                    dt = self.parse_time(ts)
                    if self.recording_start <= dt <= self.recording_stop:
                        off = (dt - self.recording_start).total_seconds()
                        self.logs.append((off, arg.text.strip()))

    def collected_logs(self):
        tree = ET.parse(self.latest_xml)
        root = tree.getroot()
        log_lines = []
        for kw in root.iter('kw'):
            if kw.attrib.get('name') == 'Log To Console':
                arg = kw.find('arg')
                status = kw.find('status')
                if arg is not None and status is not None and arg.text is not None:
                    ts = status.attrib.get('start')
                    dt = self.parse_time(ts)
                    if self.recording_start <= dt <= self.recording_stop:
                        off = (dt - self.recording_start).total_seconds()
                        msg = arg.text.strip()
                        self.logs.append((off, msg))
                        log_lines.append(f"[{off:.2f} s] {msg}")

        # Write all logs to a text file
        log_file = os.path.join(self.output_dir, "console_logs.txt")
        with open(log_file, "w", encoding="utf-8") as f:
            for line in log_lines:
                f.write(line + "\n")

        print(f"Collected {len(self.logs)} console messages. Written to {log_file}")

    def get_latest_video(self):
        mp4s = glob.glob(os.path.join(self.video_dir, "*.mp4"))
        if not mp4s:
            raise FileNotFoundError(f"No .mp4 files in {self.video_dir}")
        self.input_video = max(mp4s, key=os.path.getmtime)
        return self.input_video

    def generate_output_path(self):
        base, ext = os.path.splitext(os.path.basename(self.input_video))
        self.output_video = os.path.join(self.output_dir, f"{base}{ext}")
        return self.output_video

    def create_drawtext_filters(self):
        filters = []

        # Sanitize the font path for FFmpeg's filter syntax
        font_path_ffmpeg = self.font_path.replace('\\', '/')
        font_path_ffmpeg = font_path_ffmpeg.replace(':', '\\:')

        # A) console messages
        for t, msg in self.logs:
            # More robustly escape single quotes for FFmpeg
            safe = msg.replace("'", "'\\''")
            filters.append(
                f"drawtext=fontfile='{font_path_ffmpeg}':text='{safe}':"
                f"enable='between(t,{t:.2f},{t + 2:.2f})':"
                "x=(w-text_w)/2:y=h-th-40:fontsize=35:fontcolor=white:"
                "box=1:boxcolor=black@0.5"
            )

        # B) test-case names
        for i, (start, end, nm) in enumerate(self.testcases, start=1):
            # Also apply the same escaping here for safety
            # safe = nm.replace("'", "'\\''")
            new_text = f"Test Case {i} : {nm}"
            safe = new_text.replace("'", "\\").replace(":", "\\:")
            filters.append(
                f"drawtext=fontfile='{font_path_ffmpeg}':text='{safe}':"
                f"enable='between(t,{start:.2f},{end:.2f})':"
                "x=(w-text_w)/2:y=10:fontsize=30:fontcolor=white:"
                "box=1:boxcolor=black@0.7"
            )

        # C) running clock - Escape curly braces for f-string
        filters.append(
            f"drawtext=fontfile='{font_path_ffmpeg}':"
            "text='%{{pts\\:hms}}':x=10:y=10:fontsize=20:fontcolor=white:"
            "box=1:boxcolor=black@0.5"
        )

        return ",".join(filters)

    def run_ffmpeg(self):
        self.generate_output_path()
        fg = self.create_drawtext_filters()
        cmd = [
            "ffmpeg", "-y", "-i", self.input_video,
            "-vf", fg, "-c:a", "copy", self.output_video
        ]
        print("Running FFmpeg:", " ".join(cmd))
        subprocess.run(cmd, check=True)
        print("Overlay complete:", self.output_video)

    def run(self):
        self.xml_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/STB05_DWI859ETI/Report"
        self.video_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/STB05_DWI859ETI"
        # Set the new output directory
        self.output_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/STB05_DWI859ETI/OutputRecordings"
        os.makedirs(self.output_dir, exist_ok=True)

        print("XML →", self.get_latest_xml())
        self.parse_xml()
        print("Recording from", self.recording_start, "to", self.recording_stop)

        print("Parsing test cases…")
        self.parse_testcases()
        print(f"Found {len(self.testcases)} test cases")

        print("Collecting console logs…")
        self.collect_logs()
        print(f"Collected {len(self.logs)} console messages")
        self.collected_logs()
        print("Video →", self.get_latest_video())
        self.run_ffmpeg()


if __name__ == "__main__":
    

    # XML_DIR = r"/home/User"
    # OUT_VID_DIR = r"/home/User/Record"

    overlay = VideoLogOverlay()
    overlay.run()
 