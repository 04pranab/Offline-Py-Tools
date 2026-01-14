import os
import subprocess
import sys

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

def time_to_ffmpeg_format(t):
    """Convert hh:mm:ss or mm:ss into hh:mm:ss string."""
    parts = t.split(":")
    parts = [int(x) for x in parts]
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m, s = 0, parts[0], parts[1]
    else:
        h, m, s = 0, 0, parts[0]
    return f"{h:02d}:{m:02d}:{s:02d}"

def trim_video(input_file, output_file, trim_ranges):
    os.makedirs("temp_parts", exist_ok=True)
    part_files = []

    for idx, r in enumerate(trim_ranges.split(","), start=1):
        start, end = r.split("-")
        start = time_to_ffmpeg_format(start.strip())
        end = time_to_ffmpeg_format(end.strip())

        part_file = f"temp_parts/part{idx}.mp4"
        part_files.append(part_file)

        # Copy video, re-encode audio for best sync/quality
        cmd = [
            "ffmpeg", "-y",
            "-ss", start, "-to", end,
            "-i", input_file,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            part_file
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Make concat list
    file_list = "temp_parts/parts.txt"
    with open(file_list, "w") as f:
        for pf in part_files:
            f.write(f"file '{os.path.abspath(pf)}'\n")

    # Concatenate (video copied, audio re-encoded)
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", file_list,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        output_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Cleanup
    for pf in part_files:
        os.remove(pf)
    os.remove(file_list)
    os.rmdir("temp_parts")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python trimmer.py \"0:10:20-0:33:30,0:50:20-0:56:10\"")
        sys.exit(1)

    trim_ranges = sys.argv[1]

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, f"trimmed_{filename}")
            print(f"Processing: {filename}")
            trim_video(input_path, output_path, trim_ranges)
            print(f"Saved: {output_path}")
