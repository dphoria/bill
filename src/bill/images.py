from PIL import Image
from logging import getLogger
from math import ceil
import io
import os

log = getLogger(__file__)


def get_image_data(image: Image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def compress(image: Image, max_data_size: int) -> Image:
    image = image.convert("RGBA")

    image_data = get_image_data(image)
    log.debug(f"Image data size {len(image_data)}")

    step = 0.8
    while len(image_data) > max_data_size:
        width = ceil(image.width * step)
        height = ceil(image.height * step)
        image = image.resize((width, height), Image.Resampling.HAMMING)
        image_data = get_image_data(image)
        log.debug(f"Image data size {len(image_data)}")

    return image


def load_image(image_file_path: os.PathLike) -> bytes:
    return get_image_data(compress(Image.open(image_file_path), 1024 * 1024))
