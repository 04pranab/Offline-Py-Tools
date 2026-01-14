import os
import subprocess
import re

def safe_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def video_to_audio():
    input_folder = "input"
    output_folder = "output"

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    video_exts = (
        ".mp4", ".mkv", ".avi", ".mov",
        ".flv", ".webm", ".wmv",
        ".mpg", ".mpeg", ".m4v", ".3gp"
    )

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(video_exts)]

    if not files:
        print("⚠️ No video files found in 'input' folder.")
        return

    for file in files:
        input_path = os.path.join(input_folder, file)
        base = os.path.splitext(file)[0]
        output_name = safe_filename(base) + ".mp3"
        output_path = os.path.join(output_folder, output_name)

        print(f"🎧 Extracting audio: {file} → {output_name}")

        command = [
            "ffmpeg",
            "-i", input_path,

            # Remove video completely
            "-vn",

            # High-quality audio
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            "-ar", "44100",

            # Faster processing
            "-map_metadata", "0",
            "-y",
            output_path
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ Done: {output_path}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed: {file}")

    print("\n🎉 All audio files extracted successfully!")

if __name__ == "__main__":
    video_to_audio()

