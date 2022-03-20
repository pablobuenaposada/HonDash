import csv
import os
import shutil
from collections import OrderedDict
from contextlib import nullcontext as does_not_raise
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import mock
from unittest.mock import ANY

import pytest

from backend.constants import websocket_data_dict
from backend.devices.logger.constants import (
    CHUNKSIZE,
    DATALOGS_PATH,
    MIN_STORAGE_AVAILABLE,
)
from backend.devices.logger.exceptions import NotEnoughSpace
from backend.devices.logger.logger import Logger


class TestLogger:
    class FakeEcu:
        bat = 13.4
        gear = 0
        iat = {"celsius": 40}
        tps = 50
        ect = {"celsius": 150}
        rpm = 1000
        vss = {"kmh": 120}
        o2 = {"lambda": 1.05}
        cam = -20
        mil = False
        fanc = True
        bksw = False
        flr = True
        vtp = False
        vts = True
        vtec = "off"
        eth = 0
        scs = False
        firmware = "0.00"
        map = {"bar": 1.6}
        name = "K-Pro"

    class FakeLogger:
        active = True

    data = websocket_data_dict(
        FakeEcu(),
        "celsius",
        "celsius",
        "kmh",
        "lambda",
        "bar",
        lambda x: 2.55,
        "",
        80456,
        "day",
        "1.1.1",
        FakeLogger(),
    )

    @classmethod
    def teardown_method(self):
        """
        Delete any remaining datalog file created
        """
        for filename in os.listdir(DATALOGS_PATH):
            file_path = os.path.join(DATALOGS_PATH, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

    @pytest.mark.parametrize(
        "data, expected",
        (
            ({}, {"time": ANY}),
            ({"boolean": True}, {"time": ANY, "boolean": 1}),
            ({"string": "foo"}, {"time": ANY, "string": "foo"}),
        ),
    )
    def test__prepare_data(self, data, expected):
        original_data = data.copy()
        assert Logger._prepare_data(data, 0.0) == expected
        assert data == original_data  # original data should not be modified

    @pytest.mark.parametrize(
        "free_space, expected",
        (
            (MIN_STORAGE_AVAILABLE, True),
            (MIN_STORAGE_AVAILABLE - 1, False),
        ),
    )
    def test__check_free_space(self, free_space, expected):
        with mock.patch("shutil.disk_usage") as m_disk_usage:
            m_disk_usage.return_value = (None, None, free_space)
            assert Logger._check_free_space() is expected

    @pytest.mark.parametrize(
        "files_size, min_storage_available, remain_files_size, exception",
        (
            ([], 0, [], does_not_raise()),
            (
                [2000000, 1000000, 3000000],
                1000000,
                [1000000, 3000000],
                does_not_raise(),
            ),
            ([2000000, 1000000, 3000000], 2500000, [3000000], does_not_raise()),
            (
                [2000000, 1000000, 3000000],
                9000000,
                [],
                pytest.raises(NotEnoughSpace),
            ),  # asking for more space than possible
        ),
    )
    def test__free_space(
        self, files_size, min_storage_available, remain_files_size, exception
    ):
        # create temporal csv's
        for file_size in files_size:
            file = NamedTemporaryFile(dir=DATALOGS_PATH, suffix=".csv", delete=False)
            file.write(b"\0" * file_size)
            file.flush()
        assert len(files_size) == len(os.listdir(DATALOGS_PATH))

        _, _, free = shutil.disk_usage(f"{DATALOGS_PATH}/")
        with mock.patch(
            "backend.devices.logger.logger.MIN_STORAGE_AVAILABLE",
            new=free + min_storage_available,
        ), exception:
            Logger._free_space()
        sorted_files = sorted(
            Path(DATALOGS_PATH).iterdir(), key=os.path.getmtime
        )  # get current files
        assert [os.path.getsize(file) for file in sorted_files] == remain_files_size

    def test_log(self):
        logger = Logger()
        logger.active = True

        assert not os.path.exists(logger.file_name)
        for _ in range(CHUNKSIZE - 1):
            logger.log(self.data)
            assert not os.path.exists(logger.file_name)
        logger.log(self.data)  # this last one should create a csv file
        assert os.path.exists(logger.file_name)

        # check csv content
        with open(logger.file_name, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            assert csv_reader.fieldnames == list(self.data.keys())  # check header
            line_count = 0
            for row in csv_reader:
                assert row == OrderedDict(
                    [
                        ("bat", str(self.data["bat"])),
                        ("gear", str(self.data["gear"])),
                        ("iat", str(self.data["iat"])),
                        ("tps", str(self.data["tps"])),
                        ("ect", str(self.data["ect"])),
                        ("rpm", str(self.data["rpm"])),
                        ("vss", str(self.data["vss"])),
                        ("o2", str(self.data["o2"])),
                        ("cam", str(self.data["cam"])),
                        ("mil", str(int(self.data["mil"]))),
                        ("fan", str(int(self.data["fan"]))),
                        ("bksw", str(int(self.data["bksw"]))),
                        ("flr", str(int(self.data["flr"]))),
                        ("vtp", str(int(self.data["vtp"]))),
                        ("vts", str(int(self.data["vts"]))),
                        ("vtec", str(self.data["vtec"])),
                        ("eth", str(self.data["eth"])),
                        ("scs", str(int(self.data["scs"]))),
                        ("fmw", str(self.data["fmw"])),
                        ("map", str(self.data["map"])),
                        ("an0", str(self.data["an0"])),
                        ("an1", str(self.data["an1"])),
                        ("an2", str(self.data["an2"])),
                        ("an3", str(self.data["an3"])),
                        ("an4", str(self.data["an4"])),
                        ("an5", str(self.data["an5"])),
                        ("an6", str(self.data["an6"])),
                        ("an7", str(self.data["an7"])),
                        ("time", ANY),
                        ("odo", str(self.data["odo"])),
                        ("style", self.data["style"]),
                        ("name", self.data["name"]),
                        ("ver", self.data["ver"]),
                        ("hddlg", str(int(self.data["hddlg"]))),
                    ]
                )
                line_count += 1
        assert line_count == CHUNKSIZE

    def test_log_multiple_chunksize(self):
        """
        Checks that more than 1 chunksize lines gets saved correctly
        """
        logger = Logger()
        logger.active = True

        for _ in range(CHUNKSIZE * 2):
            logger.log(self.data)

        with open(logger.file_name, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            assert csv_reader.fieldnames == list(self.data.keys())  # check header
            assert len(list(csv_reader)) == CHUNKSIZE * 2

    def test_log_no_free_space(self):
        """If there's no space from the start, no log should be created"""
        with mock.patch("shutil.disk_usage") as m_disk_usage:
            m_disk_usage.return_value = (None, None, 0)
            logger = Logger()

            assert not os.path.exists(logger.file_name)
            for _ in range(CHUNKSIZE):
                logger.log(self.data)
            assert not os.path.exists(logger.file_name)
            assert len(logger.df) == 0  # data frame also empty

    def test_get_logs(self):
        # create temporal csv's
        for file_size in [2000000, 1000000, 3000000]:
            file = NamedTemporaryFile(dir=DATALOGS_PATH, suffix=".csv", delete=False)
            file.write(b"\0" * file_size)
            file.flush()
        assert len([2000000, 1000000, 3000000]) == len(os.listdir(DATALOGS_PATH))

        assert Logger.get_logs() == [
            (file.name, "0:00:00")
            for file in sorted(Path(DATALOGS_PATH).iterdir(), key=os.path.getmtime)
        ]

    @pytest.mark.parametrize(
        "files_name, file_name, content",
        (
            ([], "foo.csv", None),
            (["foo.csv"], "foo.csv", "bar"),
        ),
    )
    def test_get_log(self, files_name, file_name, content):
        # create temporal csv's
        for file_name in files_name:
            f = open(f"{DATALOGS_PATH}/{file_name}", "a")
            f.write(content)
            f.close()
        assert len(files_name) == len(os.listdir(DATALOGS_PATH))

        assert Logger.get_log(file_name) == content
