from pathlib import Path
from commandlib import Command


def convert_to_slow_gif(webm_path: Path):
    """
    Convert playwright's webm to a gif that plays at a reasonable
    speed with a file size that is reasonably small.

    GIFs are necessary because github's markdown doesn't seem to
    play anything else on loop.
    """
    gif_path = webm_path.parent / f"{webm_path.stem}.gif"
    palette_path = webm_path.parent / "palette.png"

    ffmpeg = Command("ffmpeg", "-y")
    ffmpeg("-i", webm_path, "-vf", "palettegen", palette_path).output()
    ffmpeg(
        "-i",
        webm_path,
        "-i",
        palette_path,
        "-filter_complex",
        "paletteuse",
        "-r",
        "10",
        gif_path,
    ).output()
    Command("convert", "-delay", "40x100", gif_path, gif_path).run()
    webm_path.unlink()
    palette_path.unlink()
