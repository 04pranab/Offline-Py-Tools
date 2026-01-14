import os
import subprocess
import re

def safe_filename(name: str) -> str:
    """Remove unsafe characters for Java phones"""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def convert_for_lava_gen10():
    input_folder = "input"
    output_folder = "output"

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    video_exts = (
        ".mp4", ".mkv", ".avi", ".mov",
        ".flv", ".webm", ".wmv",
        ".mpg", ".mpeg", ".m4v"
    )

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(video_exts)]

    if not files:
        print("⚠️ No videos found in 'input' folder.")
        return

    for file in files:
        input_path = os.path.join(input_folder, file)
        base_name = os.path.splitext(file)[0]
        output_name = safe_filename(base_name) + ".3gp"
        output_path = os.path.join(output_folder, output_name)

        print(f"🔄 Converting: {file} → {output_name}")

        command = [
            "ffmpeg",
            "-i", input_path,

            # SCALE + LETTERBOX (NO STRETCH)
            "-vf",
            "scale=320:240:force_original_aspect_ratio=decrease,"
            "pad=320:240:(ow-iw)/2:(oh-ih)/2",

            # Java phone friendly settings
            "-r", "15",
            "-pix_fmt", "yuv420p",

            "-c:v", "mpeg4",
            "-b:v", "250k",

            "-c:a", "aac",
            "-ar", "8000",
            "-b:a", "48k",

            "-y",
            output_path
        ]

        try:
            subprocess.run(command, check=True)
            print(f"✅ Saved: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {file}")
            print(e)

    print("\n🎉 All videos converted for Lava Gen 10 Power!")

if __name__ == "__main__":
    convert_for_lava_gen10()
