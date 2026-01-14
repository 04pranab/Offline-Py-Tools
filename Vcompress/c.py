import os
import subprocess

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

VIDEO_EXTENSIONS = (".mp4", ".mov", ".mkv", ".avi")

for file in os.listdir(INPUT_DIR):
    if file.lower().endswith(VIDEO_EXTENSIONS):
        in_path = os.path.join(INPUT_DIR, file)
        out_path = os.path.join(
            OUTPUT_DIR, os.path.splitext(file)[0] + ".mp4"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", in_path,
            "-c:v", "libx264",
            "-preset", "ultrafast",   # 🔥 SPEED KING
            "-crf", "27",             # acceptable web quality
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "96k",
            "-movflags", "+faststart",
            out_path
        ]

        print(f"🚀 Ultra-fast compressing: {file}")
        subprocess.run(cmd)

print("✅ DONE — fastest possible compression on old laptop.")
