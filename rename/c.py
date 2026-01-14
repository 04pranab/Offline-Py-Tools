import os
import shutil

# Folder names (same directory as this script)
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Supported image extensions
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")

# Get and sort images
images = sorted([
    f for f in os.listdir(INPUT_DIR)
    if f.lower().endswith(IMAGE_EXTENSIONS)
])

# Rename and copy images
for index, filename in enumerate(images, start=1):
    ext = os.path.splitext(filename)[1]
    new_name = f"swami-{index}{ext}"

    src_path = os.path.join(INPUT_DIR, filename)
    dst_path = os.path.join(OUTPUT_DIR, new_name)

    shutil.copy2(src_path, dst_path)

print(f"✅ Done! Renamed {len(images)} photos and saved to '{OUTPUT_DIR}' folder.")
