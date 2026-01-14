import os
import subprocess
import sys

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

def time_fmt(t):
    p = list(map(int, t.split(":")))
    if len(p) == 3:
        h, m, s = p
    elif len(p) == 2:
        h, m, s = 0, p[0], p[1]
    else:
        h, m, s = 0, 0, p[0]
    return f"{h:02d}:{m:02d}:{s:02d}"

def trim_audio(input_file, output_file, ranges):
    os.makedirs("tmp_audio", exist_ok=True)
    parts = []

    for i, r in enumerate(ranges.split(","), 1):
        start, end = r.split("-")
        part = f"tmp_audio/part{i}.m4a"
        parts.append(part)

        cmd = [
            "ffmpeg", "-y",
            "-ss", time_fmt(start.strip()),
            "-to", time_fmt(end.strip()),
            "-i", input_file,
            "-c:a", "aac",
            "-b:a", "256k",
            part
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open("tmp_audio/list.txt", "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "tmp_audio/list.txt",
        "-c:a", "aac", "-b:a", "256k",
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for p in parts:
        os.remove(p)
    os.remove("tmp_audio/list.txt")
    os.rmdir("tmp_audio")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audio_trimmer.py \"0:10-0:45,1:20-2:10\"")
        sys.exit(1)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    ranges = sys.argv[1]

    for f in os.listdir(INPUT_FOLDER):
        if f.lower().endswith((".mp3", ".wav", ".m4a", ".aac", ".flac")):
            trim_audio(
                os.path.join(INPUT_FOLDER, f),
                os.path.join(OUTPUT_FOLDER, "trimmed_" + f),
                ranges
            )
