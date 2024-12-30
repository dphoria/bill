from bill.images import load_image
from PIL import Image
import os
import pytest


def create_image_file(width: int, height: int, image_file_path: os.PathLike):
    image = Image.new("RGB", (width, height))  # Red color
    image.save(image_file_path)


@pytest.mark.parametrize("width,height", [(4000, 3000), (400, 300)])
def test_resize(width, height, tmp_path):
    image_file_path = tmp_path / "image.png"
    create_image_file(width, height, image_file_path)
    image_data = load_image(image_file_path)
    assert len(image_data) <= 1024 * 1024
