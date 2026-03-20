#!/usr/bin/env python3
"""
optimize_images.py — Compress large photography images for web delivery.

Usage:
    pip install Pillow
    python optimize_images.py

How it decides what to optimize:
    - Any image ABOVE 1.5 MB gets resized + compressed
    - Any image AT or BELOW 1.5 MB is already web-ready and gets skipped
    - Safe to run as many times as you want — small files are never touched

Workflow:
    1. Drop new photos into the images/ folders
    2. Run this script
    3. git add . && git commit -m "add photos" && git push
"""

import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run:  pip install Pillow")
    exit(1)

# === CONFIG ===
SIZE_THRESHOLD_MB = 1.5     # only optimize files larger than this
MAX_LONG_EDGE = 2000        # resize longest side to this (pixels)
JPEG_QUALITY = 82           # 80-85 is the sweet spot for quality vs size

IMAGE_DIRS = [
    "images/portfolio",
    "images/street",
    "images/landscape",
    "images/cityscape",
    "images/random",
    "images/old",
]
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


def size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def optimize(path):
    ext = Path(path).suffix.lower()
    img = Image.open(path)

    if img.mode in ("RGBA", "P") and ext in (".jpg", ".jpeg"):
        img = img.convert("RGB")

    w, h = img.size
    if max(w, h) > MAX_LONG_EDGE:
        ratio = MAX_LONG_EDGE / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    if ext in (".jpg", ".jpeg"):
        img.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True)
    elif ext == ".png":
        img.save(path, "PNG", optimize=True)
    elif ext == ".webp":
        img.save(path, "WEBP", quality=JPEG_QUALITY)


def main():
    total_saved = 0
    optimized = 0
    skipped = 0

    for d in IMAGE_DIRS:
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if Path(f).suffix.lower() not in SUPPORTED:
                continue

            src = os.path.join(d, f)
            before = size_mb(src)

            if before <= SIZE_THRESHOLD_MB:
                print(f"  SKIP  {f}  ({before:.2f} MB — already under {SIZE_THRESHOLD_MB} MB)")
                skipped += 1
                continue

            optimize(src)
            after = size_mb(src)
            saved = before - after
            total_saved += saved
            optimized += 1
            print(f"  DONE  {f}:  {before:.2f} MB -> {after:.2f} MB  (saved {saved:.2f} MB)")

    print(f"\n{'='*55}")
    if optimized > 0:
        print(f"  Optimized:  {optimized} image(s)")
        print(f"  Saved:      {total_saved:.1f} MB total")
    else:
        print(f"  Nothing to do — all images are under {SIZE_THRESHOLD_MB} MB")
    if skipped > 0:
        print(f"  Skipped:    {skipped} image(s) (already small enough)")
    print(f"  Threshold:  {SIZE_THRESHOLD_MB} MB  |  Max edge: {MAX_LONG_EDGE}px  |  Quality: {JPEG_QUALITY}")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
