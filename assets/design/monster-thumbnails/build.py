"""Build uniform thumbnails from the sprite resources already referenced by the game."""

from __future__ import annotations

import concurrent.futures
import hashlib
import io
import json
import struct
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source-manifest.json"
SIZE = 256
ART_SIZE = 216
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CDN = "https://mod-resource.dn.nexoncdn.co.kr/"


def extract_png(container: bytes) -> bytes:
    start = container.find(PNG_SIGNATURE)
    if start < 0:
        raise ValueError("Resource does not contain a PNG")
    position = start + len(PNG_SIGNATURE)
    while position + 12 <= len(container):
        length = struct.unpack_from(">I", container, position)[0]
        chunk_type = container[position + 4 : position + 8]
        position += 12 + length
        if chunk_type == b"IEND":
            return container[start:position]
    raise ValueError("Resource PNG has no IEND chunk")


def fetch_original(path: str) -> Image.Image:
    url = CDN + path
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            image = Image.open(io.BytesIO(extract_png(data)))
            image.load()
            return image.convert("RGBA")
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt == 3:
                raise RuntimeError(f"Failed to fetch {path}: {error}") from error
            time.sleep(0.6 * 2**attempt)
    raise AssertionError("unreachable")


def build_one(row: dict) -> dict:
    original = fetch_original(row["pngModPath"])
    alpha = original.getchannel("A").point(lambda value: 255 if value > 8 else 0)
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError(f"Empty sprite: {row['id']}")
    art = original.crop(bbox)
    scale = min(ART_SIZE / art.width, ART_SIZE / art.height)
    width = max(1, round(art.width * scale))
    height = max(1, round(art.height * scale))
    resampling = Image.Resampling.LANCZOS if scale < 1 else Image.Resampling.NEAREST
    art = art.resize((width, height), resampling)
    canvas = Image.new("RGBA", (SIZE, SIZE))
    canvas.alpha_composite(art, ((SIZE - width) // 2, (SIZE - height) // 2))
    relative = f"{row['kind']}/{row['id']}.png"
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, optimize=True)
    return {
        "id": row["id"],
        "name": row["name"],
        "kind": row["kind"],
        "file": relative,
        "spriteRuid": row["spriteRuid"],
        "sourcePath": row["sourcePath"],
        "sourceSize": [original.width, original.height],
        "croppedSize": [bbox[2] - bbox[0], bbox[3] - bbox[1]],
        "artSize": [width, height],
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    }


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidate = Path("C:/Windows/Fonts/malgun.ttf")
    return ImageFont.truetype(str(candidate), size) if candidate.exists() else ImageFont.load_default()


def contact_sheet(rows: list[dict], kind: str, columns: int, cell_size: int) -> None:
    entries = [row for row in rows if row["kind"] == kind]
    cell_height = cell_size + 42
    sheet = Image.new(
        "RGB", (columns * cell_size, ((len(entries) + columns - 1) // columns) * cell_height), "#263141"
    )
    draw = ImageDraw.Draw(sheet)
    label_font = font(12 if kind == "monster" else 14)
    for index, row in enumerate(entries):
        left = (index % columns) * cell_size
        top = (index // columns) * cell_height
        draw.rounded_rectangle(
            (left + 3, top + 3, left + cell_size - 4, top + cell_height - 4),
            radius=9,
            fill="#344459",
            outline="#576b82",
        )
        icon = Image.open(ROOT / row["file"]).convert("RGBA")
        icon.thumbnail((cell_size - 12, cell_size - 12), Image.Resampling.LANCZOS)
        sheet.paste(icon, (left + (cell_size - icon.width) // 2, top + (cell_size - icon.height) // 2), icon)
        label = f"{row['id']} {row['name']}"
        draw.text((left + cell_size // 2, top + cell_size + 4), label, font=label_font, fill="white", anchor="mt")
    sheet.save(ROOT / f"contact-sheet-{kind}.jpg", quality=90, optimize=True)


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    ids = [row["id"] for row in source]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate monster ID")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(build_one, row): row for row in source}
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            row = futures[future]
            try:
                result = future.result()
            except Exception as error:
                print(f"ERROR {row['id']} {row['name']}: {error}", flush=True)
                raise
            results.append(result)
            if index % 25 == 0 or index == len(source):
                print(f"Built {index}/{len(source)}", flush=True)
    ordering = {id_: index for index, id_ in enumerate(ids)}
    results.sort(key=lambda row: ordering[row["id"]])
    (ROOT / "manifest.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    contact_sheet(results, "monster", 10, 110)
    contact_sheet(results, "boss", 6, 176)
    print(f"Complete: {len(results)} thumbnails", flush=True)


if __name__ == "__main__":
    main()
