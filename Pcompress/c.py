import os
import subprocess
from PIL import Image

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPORTED = (".jpg", ".jpeg", ".png")

for file in os.listdir(INPUT_DIR):
    if not file.lower().endswith(SUPPORTED):
        continue

    input_path = os.path.join(INPUT_DIR, file)
    output_path = os.path.join(OUTPUT_DIR, file)

    ext = file.lower().split(".")[-1]

    # Convert everything to optimized RGB first (fast & clean)
    img = Image.open(input_path).convert("RGB")
    img.save(output_path, optimize=True, quality=92)

    # JPEG → libjpeg-turbo (SUPER FAST)
    if ext in ("jpg", "jpeg"):
        subprocess.run([
            "jpegoptim",
            "--strip-all",
            "--max=92",
            "--all-progressive",
            output_path
        ], stdout=subprocess.DEVNULL)

    # PNG → pngquant (BEST compression, visually lossless)
    elif ext == "png":
        subprocess.run([
            "pngquant",
            "--quality=85-95",
            "--speed", "1",
            "--force",
            "--output", output_path,
            output_path
        ], stdout=subprocess.DEVNULL)

print("✅ Ultra-fast compression complete. Website-ready images in /output")

