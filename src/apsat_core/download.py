# Apsat  Copyright (C) 2026  Deswatts<Deswatts_Cre@outlook.com>
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.


import hashlib
import math
import os
import threading

import requests

from deswatts_tools import logutil

logger = logutil.setup_logger(__name__)


class DownloadEngine:
    def __init__(self, download_list: list, download_thread: int = 8):
        """
        Multi thread download engine

        :param download_list: Download task list
        :param download_thread: Max thread count
        :raises ValueError: When you call some unsupport hash type(exam: md5)

        Param download_list example:

        .. code:: json

            [
                {
                    "filename": "example.png",
                    "url": "https://example.com/example.png",
                    "sha256": "add0613512f1b7f485f3fe445ae0bfcd344293dbea23e4bf2f999e0f97b80176"
                },
                ...
            ]
        """
        super().__init__()

        if not download_list:
            raise ValueError("The param download_list is Empty")

        download_list_tmp = download_list
        downloads = []
        for i in range(math.ceil(len(download_list) / download_thread)):
            if len(download_list_tmp) == 0:
                break

            downloads.append(download_list_tmp[0:download_thread])
            for j in range(download_thread):
                try:
                    download_list_tmp.pop(0)
                except IndexError:
                    break

        threads = []
        for i in range(len(downloads)):
            threads.append(
                threading.Thread(
                    target=self.download_unit, name=f"Download-{i}", args=[downloads[i]]
                )
            )
        for i in threads:
            i.start()
        for i in threads:
            i.join()

    @staticmethod
    def download_unit(download_list: list):
        for i in download_list:
            if "sha256" in i:
                check = DownloadEngine.check_sha256(i)
            elif "sha1" in i:
                check = DownloadEngine.check_sha1(i)
            else:
                raise ValueError("Unsupport hash type")

            url = i["url"]
            filename = i["file_name"] if "file_name" in i else i["filename"]

            if not check:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(filename, "wb") as f:
                        f.writelines(r.iter_content(chunk_size=4096))

                logger.info(f"Downloaded: {os.path.abspath(filename)}")
            else:
                logger.info(f"{os.path.abspath(filename)} is exists")

    @staticmethod
    def check_sha256(task: dict[str, str]):
        filename = task["file_name"] if "file_name" in task else task["filename"]
        target_sha256 = task["sha256"]

        if not os.path.exists(filename):
            return False
        if filename is os.PathLike:
            filename = str(filename)

        file_hash = hashlib.sha256()

        with open(filename, "rb+") as f:
            while True:
                tmp = f.read(4096)
                if tmp == b"":
                    break

                file_hash.update(tmp)

        return file_hash.hexdigest() == target_sha256

    @staticmethod
    def check_sha1(task: dict[str, str]):
        filename = task["file_name"]
        target_sha1 = task["sha1"]

        if not os.path.exists(filename):
            return False
        if filename is os.PathLike:
            filename = str(filename)

        file_hash = hashlib.sha1()

        with open(filename, "rb+") as f:
            while True:
                tmp = f.read(4096)
                if tmp == b"":
                    break

                file_hash.update(tmp)

        return file_hash.hexdigest() == target_sha1
