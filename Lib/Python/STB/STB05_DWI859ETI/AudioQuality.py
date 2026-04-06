# import soundfile as sf
# import numpy as np
# import subprocess
# import time

# class AudioQuality:
#     def __init__(self):
#         pass

#     def record_audio(self, device="hw:1,0", duration=5, filename="/tmp/audio_test.wav"):
#         """
#         Records audio using arecord for the specified duration and device.
#         """
#         cmd = [
#             "arecord", "-D", device, "-d", str(duration),
#             "-f", "S16_LE", "-c", "2", "-r", "48000", filename
#         ]
#         subprocess.run(cmd, check=True)

#     def analyze_audio(self, filename="/tmp/audio_test.wav"):
#         """
#         Analyzes audio file and returns RMS value, or None if no audio detected.
#         """
#         data, _ = sf.read(filename)
#         mono = np.mean(data, axis=1)

#         rms = np.sqrt(np.mean(mono ** 2))
#         if rms < 0.001:  # threshold for silence
#             return None

#         return rms

#     def classify_audio(self, rms_avg):
#         """
#         Classifies audio based on average RMS.
#         0 = No audio, 1 = Low, 2 = High
#         """
#         if rms_avg is None:
#             return 0
#         elif rms_avg < 0.01:
#             return 0  # effectively muted
#         elif rms_avg < 0.05:
#             return 1  # low audio
#         else:
#             return 2  # high audio

#     def check_audio_quality(self, device="hw:1,0", checks=3, duration=5, wait=5):
#         """
#         Records multiple times, calculates average RMS, and returns:
#         0 = No audio
#         1 = Low
#         2 = High
#         """
#         rms_values = []
#         for i in range(checks):
#             print(f"Recording {i+1}/{checks}...")
#             cmd = [
#                 "arecord", "-D", device, "-d", str(duration),
#                 "-f", "S16_LE", "-c", "2", "-r", "48000", "/tmp/audio_test.wav"
#             ]
#             subprocess.run(cmd, check=True)

#             data, _ = sf.read("/tmp/audio_test.wav")
#             mono = np.mean(data, axis=1)
#             rms = np.sqrt(np.mean(mono ** 2))
#             if rms > 0.001:  # valid audio
#                 rms_values.append(rms)

#             time.sleep(wait)

#         if not rms_values:
#             return 0
#         avg_rms = sum(rms_values) / len(rms_values)
#         if avg_rms < 0.01:
#             return 0
#         elif avg_rms < 0.05:
#             return 1
#         else:
#             return 2
        
# if __name__ == "__main__":
#     aq = AudioQuality()
#     result = aq.check_audio_quality(device="hw:1,0", checks=3, duration=5, wait=5)
#     print(f"\nFinal Audio Quality Result: {result}")
#     if result == 0:
#         print("Audio is muted / no audio")
#     elif result == 1:
#         print("Audio is low")
#     elif result == 2:
#         print("Audio is high")


import soundfile as sf
import numpy as np
import subprocess
import time
import os

class AudioQuality:
    def __init__(self):
        self.filename = "/tmp/audio_test.wav"

    def record_audio(self, device="hw:1,0", duration=5):
        """
        Records audio using arecord for the specified duration and device.
        """
        cmd = [
            "arecord", "-D", device, "-d", str(duration),
            "-f", "S16_LE", "-c", "2", "-r", "48000", self.filename
        ]
        subprocess.run(cmd, check=True)

    def compute_rms(self, data):
        """
        Computes RMS from stereo data using max of channels after DC offset removal.
        """
        if data.ndim == 1:
            mono = data - np.mean(data)
            return np.sqrt(np.mean(mono ** 2))

        left = data[:, 0] - np.mean(data[:, 0])
        right = data[:, 1] - np.mean(data[:, 1])
        rms_left = np.sqrt(np.mean(left ** 2))
        rms_right = np.sqrt(np.mean(right ** 2))
        return max(rms_left, rms_right)

    def analyze_audio(self):
        """
        Analyzes audio file and returns RMS value, or None if no audio detected.
        """
        if not os.path.exists(self.filename):
            return None

        data, _ = sf.read(self.filename)
        rms = self.compute_rms(data)
        return rms if rms > 0.001 else None

    def classify_audio(self, rms_avg):
        """
        Classifies audio based on average RMS.
        0 = No audio, 1 = Low, 2 = High
        """
        if rms_avg is None or rms_avg < 0.005:
            return 0  # No audio
        elif rms_avg < 0.0081:
            return 1  # Low
        else:
            return 2  # High

    def check_audio_quality(self, device="hw:1,0", checks=3, duration=5, wait=5):
        """
        Records multiple times, calculates average RMS, and returns:
        0 = No audio, 1 = Low, 2 = High
        """
        rms_values = []
        for i in range(checks):
            print(f"Recording {i+1}/{checks}...")
            self.record_audio(device=device, duration=duration)
            rms = self.analyze_audio()
            if rms:
                print(f"RMS {i+1}: {rms:.4f}")
                rms_values.append(rms)
            else:
                print(f"RMS {i+1}: No audio detected")
            time.sleep(wait)

        if not rms_values:
            return 0

        avg_rms = sum(rms_values) / len(rms_values)
        print(f"Average RMS: {avg_rms:.4f}")
        return self.classify_audio(avg_rms)

# Example usage
if __name__ == "__main__":
    aq = AudioQuality()
    quality = aq.check_audio_quality()
    print(f"Audio Quality: {['No Audio', 'Low', 'High'][quality]}")