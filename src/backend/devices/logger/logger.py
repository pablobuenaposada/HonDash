import datetime
import os
import shutil
import time
import uuid
from pathlib import Path

import pandas as pd
from pandas._libs.parsers import EmptyDataError

from backend.devices.logger.constants import (
    CHUNKSIZE,
    DATALOGS_PATH,
    MAX_CHUNK_SIZE_PER_FILE,
    MIN_STORAGE_AVAILABLE,
)
from backend.devices.logger.exceptions import NotEnoughSpace


def get_file_path(file_name=None):
    if file_name is None:
        file_name = f"{uuid.uuid4().hex}.csv"
    return f"{DATALOGS_PATH}/{file_name}"


class Logger:
    df = pd.DataFrame()
    active = False
    number_of_chunks = 0
    start_time = time.perf_counter()
    file_name = get_file_path()

    def __init__(self, autostart=False):
        self.autostart = autostart

    @staticmethod
    def get_logs():
        files = sorted(Path(DATALOGS_PATH).iterdir(), key=os.path.getmtime)
        files = [
            file for file in files if file.suffix == ".csv"
        ]  # remove all not csv files
        files_info = []
        for file in files:
            try:
                df = pd.read_csv(get_file_path(file.name))
                files_info.append(
                    (
                        file.name,
                        str(datetime.timedelta(seconds=int(df.tail(1)["time"]))),
                    )
                )
            except (KeyError, ValueError, EmptyDataError):
                files_info.append((file.name, "0:00:00"))
        return files_info

    @staticmethod
    def get_log(file_name):
        try:
            file = open(get_file_path(file_name), "r")
        except FileNotFoundError:
            return None
        return file.read()

    @staticmethod
    def remove_log(file_name):
        os.remove(f"{DATALOGS_PATH}/{file_name}")

    @staticmethod
    def _check_free_space():
        _, _, free = shutil.disk_usage(f"{DATALOGS_PATH}/")
        return free >= MIN_STORAGE_AVAILABLE

    @staticmethod
    def _free_space():
        """
        Deletes old datalog files until there's specific free space
        """
        if Logger._check_free_space():
            return
        files = sorted(Path(DATALOGS_PATH).iterdir(), key=os.path.getmtime)
        while not Logger._check_free_space() and files:
            files = sorted(Path(DATALOGS_PATH).iterdir(), key=os.path.getmtime)
            if files:
                os.remove(files[0])  # delete the oldest csv
        if not Logger._check_free_space():
            raise NotEnoughSpace

    @staticmethod
    def _prepare_data(data, start_time):
        # use deepcopy if at some point data contains lists or objects
        prepared_data = data.copy()
        for key in prepared_data:
            if type(prepared_data[key]) is bool:
                # if it's a boolean we convert it to 0 or 1
                prepared_data[key] = int(prepared_data[key])
        prepared_data["time"] = time.perf_counter() - start_time
        return prepared_data

    def toggle(self):
        self.active = not self.active
        self.df = pd.DataFrame()
        self.number_of_chunks = 0
        self.start_time = time.perf_counter()
        self.file_name = get_file_path()

    def log(self, data):
        if self.active:
            self.df = self.df.append(
                [self._prepare_data(data, self.start_time)], ignore_index=True
            )
            if len(self.df.index) >= CHUNKSIZE:  # if it's time to store in the csv
                try:
                    Logger._free_space()
                except NotEnoughSpace:
                    # if there's no more space just stop logging
                    self.df = None
                    self.active = False
                    return
                to_csv = self.df.iloc[:CHUNKSIZE, :]  # part to be stored
                # remove the part to be stored from memory
                self.df = self.df.iloc[CHUNKSIZE:, :]
                if self.number_of_chunks == 0:
                    to_csv.to_csv(self.file_name, index=False)
                else:  # here we need headers
                    to_csv.to_csv(self.file_name, mode="a", header=False, index=False)
                self.number_of_chunks += 1
                if self.number_of_chunks >= MAX_CHUNK_SIZE_PER_FILE:
                    self.number_of_chunks = 0
                    self.start_time = time.perf_counter()
                    self.file_name = get_file_path()
        else:
            if self.autostart and data["vss"] > 0:
                self.autostart = False
                self.active = True
