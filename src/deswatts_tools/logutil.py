# DeswattsTools  Copyright (C) 2026  Deswatts<Deswatts_Cre@outlook.com>
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.

import gzip
import logging
import os
import time

import colorama


def init(name: str) -> logging.Logger:
    """
    初始化Logger（日志器）函数
    :param name: Logger名称
    :return: Logger类
    """
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass

    now_localtime = time.localtime()
    now_time = time.strftime("%Y-%m-%d %H-%M-%S", now_localtime)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"logs/{now_time}.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    log_list = os.listdir("logs")
    for i in log_list:
        if i == f"{now_time}.log":
            continue
        file_path = os.path.abspath(os.path.join("logs", i))
        if os.path.isfile(file_path) and (os.path.basename(file_path).split(".")[-1] == "log"):
            with open(str(file_path), "rb+") as infile, \
                open(str(file_path).replace(".log", ".gz"), "wb+") as outfile:
                outfile.write(gzip.compress(infile.read()))
            try:
                os.remove(file_path)
            except PermissionError:
                pass

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    console_formatter = logging.Formatter(
        f"{colorama.Fore.LIGHTGREEN_EX}[%(asctime)s] {colorama.Fore.LIGHTCYAN_EX}[%(threadName)s:%(lineno)s/%(levelname)s]: {colorama.Fore.LIGHTWHITE_EX}%(message)s"
    )
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(threadName)s:%(lineno)s/%(levelname)s]: %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def setup_logger(name: str) -> logging.Logger:
    """
    设置Logger函数
    :param name: Logger名称
    :return: Logger类
    """
    logger = init(name)
    return logger


def remove_logs(dir_name: str | os.PathLike[str] = "logs") -> None:
    clear_list = os.listdir(dir_name)
    for i in clear_list:
        if os.path.isdir(os.path.join(dir_name, i)):
            remove_logs(os.path.join(dir_name, i))
        else:
            try:
                os.remove(os.path.join(dir_name, i))
                print(f"Deleted: {os.path.join(dir_name, i)}")
            except FileNotFoundError:
                pass
            except OSError:
                pass

    try:
        os.removedirs(dir_name)
    except OSError:
        pass