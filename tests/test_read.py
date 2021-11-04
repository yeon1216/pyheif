import glob
import io
from pathlib import Path

import piexif
from PIL import Image, ImageCms
import pyheif
import pytest


heif_files = list(Path().glob("tests/images/**/*.heic"))
hif_files = list(Path().glob("tests/images/**/*.HIF"))


@pytest.fixture(scope="session", params=heif_files)
def heif_file(request):
    return pyheif.read(request.param)


@pytest.mark.parametrize('path', heif_files)
def test_check_filetype(path):
    filetype = pyheif.check(path)
    assert pyheif.heif_filetype_no != filetype


@pytest.mark.parametrize('path', heif_files)
def test_read_file_names(path):
    heif_file = pyheif.read(str(path))
    assert heif_file is not None
    width, height = heif_file.size
    assert width > 0
    assert height > 0
    assert len(heif_file.data) > 0


@pytest.mark.parametrize('path', heif_files)
def test_read_paths(path):
    heif_file = pyheif.read(path)
    assert heif_file is not None
    width, height = heif_file.size
    assert width > 0
    assert height > 0
    assert len(heif_file.data) > 0


@pytest.mark.parametrize('path', heif_files)
def test_read_file_objects(path):
    with open(path, "rb") as f:
        heif_file = pyheif.read(f)
        assert heif_file is not None
        width, height = heif_file.size
        assert width > 0
        assert height > 0
        assert len(heif_file.data) > 0


@pytest.mark.parametrize('path', heif_files)
def test_read_bytes(path):
    with open(path, "rb") as f:
        d = f.read()
        heif_file = pyheif.read(d)
        assert heif_file is not None
        width, height = heif_file.size
        assert width > 0
        assert height > 0
        assert len(heif_file.data) > 0


@pytest.mark.parametrize('path', heif_files)
def test_read_bytearrays(path):
    with open(path, "rb") as f:
        d = bytearray(f.read())
        heif_file = pyheif.read(d)
        assert heif_file is not None
        width, height = heif_file.size
        assert width > 0
        assert height > 0
        assert len(heif_file.data) > 0


def test_read_exif_metadata(heif_file):
    for m in heif_file.metadata or []:
        if m["type"] == "Exif":
            exif_dict = piexif.load(m["data"])
            assert "0th" in exif_dict
            assert len(exif_dict["0th"]) > 0
            assert "Exif" in exif_dict
            assert len(exif_dict["Exif"]) > 0


def test_read_icc_color_profile(heif_file):
    if heif_file.color_profile and heif_file.color_profile["type"] in ["prof", "rICC"]:
        profile = io.BytesIO(heif_file.color_profile["data"])
        cms = ImageCms.getOpenProfile(profile)


def test_read_pillow_frombytes(heif_file):
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    # image.save(f"{fn}.png")


@pytest.mark.parametrize('path', hif_files)
def test_read_10_bit(path):
    heif_file = pyheif.read(path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
