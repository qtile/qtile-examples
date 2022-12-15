import os
import tempfile

import pytest

import yandexdisk as widget


@pytest.fixture
def yandexdisk_folder():
    with tempfile.TemporaryDirectory() as tmp:
        sync_folder = os.path.join(tmp, "Yandex.Disk")

        corelog_file = os.path.join(
            sync_folder,
            ".sync",
            "core.log",
        )

        status_file = os.path.join(sync_folder, ".sync", "status")
        os.makedirs(os.path.dirname(status_file), exist_ok=True)

        with open(status_file, "w") as f:
            f.write("99999\nidle")

        with open(corelog_file, "w") as f:
            f.write('21214-142356.408 DIGEST "random.dat" 9 / 10\n')

        yield sync_folder


def test_yandexdisk_idle(yandexdisk_folder):
    yandexdisk = widget.YandexDisk(sync_folder=yandexdisk_folder)
    assert yandexdisk.poll() == "IDLE"


def test_yandexdisk_stopped(yandexdisk_folder):
    yandexdisk = widget.YandexDisk(sync_folder=yandexdisk_folder)

    status_file = os.path.join(yandexdisk_folder, ".sync", "status")
    os.remove(status_file)

    assert yandexdisk.poll() == "STOPPED"


def test_yandexdisk_mapping(yandexdisk_folder):
    status_mapping = {"idle": "-.-"}

    yandexdisk = widget.YandexDisk(sync_folder=yandexdisk_folder, status_mapping=status_mapping)

    assert yandexdisk.poll() == "-.-"


def test_yandexdisk_progress(yandexdisk_folder):
    status_file = os.path.join(yandexdisk_folder, ".sync", "status")

    with open(status_file, "w") as f:
        f.write("99999\nindex")

    yandexdisk = widget.YandexDisk(sync_folder=yandexdisk_folder)

    assert yandexdisk.poll() == "INDEX (random.dat 90.0%)"
