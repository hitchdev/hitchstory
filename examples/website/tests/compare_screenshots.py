"""
Rudimentary screenshot testing done with the amazing
https://github.com/whtsky/pixelmatch-py library.

Potential improvements:

* Handle areas of the screenshot varying.
"""
from pixelmatch.contrib.PIL import pixelmatch
from hitchstory import Failure
from pathlib import Path
from io import BytesIO
from PIL import Image


def compare_screenshots(
    screenshot: bytes,
    golden_snapshot_path: Path,
    diff_snapshot_path: Path,
    threshold=0.1
):
    image = Image.open(BytesIO(screenshot))
    golden = Image.open(golden_snapshot_path)
    
    if image.width != golden.width:
        raise Failure(f"Snapshot failure. Screenshot width {image.width}, Golden master width {golden.width}")
    
    if image.height != golden.height:
        raise Failure(f"Snapshot failure. Screenshot height {image.height}, Golden master height {golden.height}")
    
    diff_pixels = pixelmatch(image, golden, threshold=threshold)
    
    # Currently failing in github actions
    if diff_pixels != 0:
        image_diff = Image.new("RGBA", image.size)
        pixelmatch(image, golden, image_diff, threshold=threshold)
        image_diff.save(diff_snapshot_path)
        raise Failure("Screenshot test failure")
