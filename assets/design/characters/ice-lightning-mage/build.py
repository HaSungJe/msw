"""Normalize the illustrated key poses into a shared game sprite coordinate system."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
FRAME_SIZE = 512
PIVOT = (256, 488)  # Feet at one consistent canvas coordinate.
SCALE = 0.35  # Same scale for every generated key pose.


def normalized(filename: str) -> Image.Image:
    source = Image.open(ROOT / "source" / filename).convert("RGBA")
    alpha = source.getchannel("A").point(lambda value: 255 if value > 16 else 0)
    box = alpha.getbbox()
    if box is None:
        raise ValueError(f"Empty source image: {filename}")
    cropped = source.crop(box)
    scaled = cropped.resize(
        (round(cropped.width * SCALE), round(cropped.height * SCALE)), Image.Resampling.LANCZOS
    )
    canvas = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    x = (FRAME_SIZE - scaled.width) // 2
    y = PIVOT[1] - scaled.height
    if x < 0 or y < 0 or x + scaled.width > FRAME_SIZE:
        raise ValueError(f"Pose is too large for the sprite canvas: {filename}")
    canvas.alpha_composite(scaled, (x, y))
    return canvas


def shifted(image: Image.Image, dy: int) -> Image.Image:
    canvas = Image.new("RGBA", image.size)
    canvas.alpha_composite(image, (0, dy))
    return canvas


def save_frame(image: Image.Image, group: str, index: int) -> str:
    path = ROOT / "frames" / group / f"{index:02d}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)
    return path.relative_to(ROOT).as_posix()


def save_preview(images: list[Image.Image], durations: list[int], filename: str) -> None:
    # GIF is for review; transparent PNG frames are the integration source.
    previews = []
    for frame in images:
        reduced = frame.resize((256, 256), Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", reduced.size, "#33465c")
        tile.alpha_composite(reduced)
        previews.append(tile.convert("RGB"))
    previews[0].save(
        ROOT / filename,
        save_all=True,
        append_images=previews[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )


def save_contact_sheet(idle: Image.Image, windup: Image.Image, release: Image.Image) -> None:
    poses = [("기본 자세", idle), ("시전 준비", windup), ("체인 라이트닝", release)]
    sheet = Image.new("RGB", (960, 400), "#29394e")
    draw = ImageDraw.Draw(sheet)
    font_path = Path("C:/Windows/Fonts/malgun.ttf")
    font = ImageFont.truetype(str(font_path), 19) if font_path.exists() else ImageFont.load_default()
    for index, (label, image) in enumerate(poses):
        x = index * 320
        draw.rounded_rectangle((x + 8, 8, x + 312, 392), radius=14, fill="#40546c", outline="#6d89a4", width=2)
        art = image.resize((320, 320), Image.Resampling.LANCZOS)
        sheet.paste(art, (x, 20), art)
        draw.text((x + 160, 355), label, fill="white", font=font, anchor="mm")
    sheet.save(ROOT / "pose-preview.png", optimize=True)


def main() -> None:
    idle = normalized("idle-master.png")
    windup = normalized("cast-windup.png")
    release = normalized("cast-release.png")

    idle_images = [shifted(idle, dy) for dy in (0, -2, -3, -1)]
    idle_durations = [180, 180, 180, 180]
    attack_images = [idle, windup, shifted(windup, -2), release, release, idle]
    attack_durations = [90, 110, 70, 100, 110, 130]

    clips = {}
    for name, images, durations in (
        ("idle", idle_images, idle_durations),
        ("chain-lightning-cast", attack_images, attack_durations),
    ):
        paths = [save_frame(image, name, i) for i, image in enumerate(images)]
        clips[name] = {"loop": name == "idle", "frames": [{"file": path, "durationMs": ms} for path, ms in zip(paths, durations)]}
        save_preview(images, durations, f"preview-{name}.gif")

    manifest = {
        "jobId": "il",
        "name": "아크메이지(썬·콜)",
        "status": "visual prototype",
        "style": "original soft cartoon chibi",
        "canvas": [FRAME_SIZE, FRAME_SIZE],
        "feetPivot": list(PIVOT),
        "direction": "right",
        "clips": clips,
    }
    (ROOT / "animation.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save_contact_sheet(idle, windup, release)
    print(f"Wrote {sum(len(clip['frames']) for clip in clips.values())} PNG frames and 2 previews")


if __name__ == "__main__":
    main()
