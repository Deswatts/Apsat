# Apsat  Copyright (C) 2026  Deswatts<Deswatts_Cre@outlook.com>
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.


import os.path
import re

import requests
import urllib3

from apsat_core import consts, get_profile_microsoft, get_profile_yggdrasil
from apsat_core.exceptions import ProfileHasNotCustomCape, ProfileHasNotCustomSkin
from apsat_core.types import (
    NameList,
    ProfileList,
    ProfileType,
    TextureUrlList,
)
from deswatts_tools import logutil

logger = logutil.setup_logger(__name__)
check_url_pattern = re.compile(r"http(s?)://")


def _yggdrasil_profile(url: str, names: NameList):
    return get_profile_yggdrasil.get_profile_yggdrasil(names, url)


def _microsoft_profile(names: NameList):
    return get_profile_microsoft.get_profile_microsoft(names)


def _get_textures(profiles: ProfileList):
    return get_profile_microsoft.get_skin(profiles)


def resolve_textures(
    textures: TextureUrlList,
    type: ProfileType | int,
    download_dir: str | os.PathLike[str] | os.PathLike[bytes],
):
    if type is ProfileType:
        type = int(type.type, 2)
    if download_dir is os.PathLike:
        download_dir = str(download_dir)
    result = []
    for i in textures:
        if type & consts.TYPE_SKIN == consts.TYPE_SKIN:
            if i["skin_url"] is None:
                raise ProfileHasNotCustomSkin

            result.append(
                {
                    "filename": os.path.join(
                        download_dir, i["profile_name"] + "-skin.png"
                    ),
                    "url": i["skin_url"]["url"],
                    "sha256": os.path.basename(
                        urllib3.util.url.parse_url(i["skin_url"]["url"]).path
                    ),
                }
            )
        elif type & consts.TYPE_CAPE == consts.TYPE_CAPE:
            if i["cape_url"] is None:
                raise ProfileHasNotCustomCape

            result.append(
                {
                    "filename": os.path.join(
                        download_dir, i["profile_name"] + "-cape.png"
                    ),
                    "url": i["cape_url"]["url"],
                    "sha256": os.path.basename(
                        urllib3.util.url.parse_url(i["cape_url"]["url"]).path
                    ),
                }
            )

    try:
        os.mkdir(download_dir)
    except FileExistsError:
        pass

    logger.info(f"Resolve the textures: {result}")

    return result


def _to_absolute_url(url: str, base: str):
    """
    This funtion returns absolute url
    :param url: target url
    :param base: base url
    :return: absolute url
    """

    if re.match(check_url_pattern, url) is not None:
        return url
    if url[0] == '/' and base[-1] == '/':
        base = base[1:]
    elif url[0] != '/' and base[-1] != '/':
        url += '/'
    return base + url


def _resolve_api_url(source_url: str):
    """
    This function returns real api url
    :param source_url: url from user input
    :return: api url
    """

    check_url = re.match(check_url_pattern, source_url)
    if check_url is None:
        source_url = "https://" + source_url

    response = requests.get(source_url)
    if "x-authlib-injector-api-location" in response.headers:
        new_url = _to_absolute_url(response.headers["x-authlib-injector-api-location"], source_url)
        if new_url != source_url:
            return new_url

    return source_url


def get_profile(
    mode: ProfileType | int, names: NameList, url: str | None = None
) -> TextureUrlList | ProfileList | None:
    if mode is ProfileType:
        mode = int(mode.type, 2)

    if (url is None) and (mode & consts.TYPE_YGGDRASIL == consts.TYPE_YGGDRASIL):
        raise ValueError("Missing url")

    if mode & consts.TYPE_YGGDRASIL == consts.TYPE_YGGDRASIL:
        url = _resolve_api_url(url)

    profiles = (
        _yggdrasil_profile(url, names)
        if mode & consts.TYPE_YGGDRASIL == consts.TYPE_YGGDRASIL
        else _microsoft_profile(names)
    )

    logger.info(f"Got profiles: {profiles}")

    if mode & consts.TYPE_PROFILE == consts.TYPE_PROFILE:
        textures = profiles
    else:
        textures = _get_textures(profiles)
        logger.info(f"Got textures: {textures}")

    return textures


if __name__ == '__main__':
    print(get_profile(1, NameList(["a"]), ""))