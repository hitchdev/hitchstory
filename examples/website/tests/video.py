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
    webm_temp = webm_path.parent / "webm_temp.webm"
    palette_path = webm_path.parent / "palette.png"

    ffmpeg = Command("ffmpeg", "-y")

    # Cut first second - just blank loading
    ffmpeg(
        "-i", webm_path, "-ss", "1", "-fflags", "+genpts", webm_temp
    ).output()

    # Convert to GIF
    ffmpeg("-i", webm_temp, "-vf", "palettegen", palette_path).output()
    ffmpeg(
        "-i",
        webm_temp,
        "-i",
        palette_path,
        "-filter_complex",
        "paletteuse",
        "-r",
        "10",
        gif_path,
    ).output()

    # Slow down GIF
    Command("convert", "-delay", "50x100", gif_path, gif_path).run()

    # Clean up
    webm_path.unlink()
    webm_temp.unlink()
    palette_path.unlink()
