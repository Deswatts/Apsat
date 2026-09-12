# Apsat  Copyright (C) 2026  Deswatts<Deswatts_Cre@outlook.com>
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.


import json
import re
from base64 import b64decode

import requests

from apsat_core.types import (
    NameList,
    ProfileList,
    TextureList,
    TextureUrlList,
    TextureUrls,
    Url,
    UUIDList,
)

_get_uuids_url = "https://api.mojang.com/profiles/minecraft"
_get_profiles_url = (
    "https://sessionserver.mojang.com/session/minecraft/profile/<UUID>?unsigned=false"
)

_replace_get_profiles_url_pattern = re.compile(r"<UUID>")


def _get_uuids(profile_names: NameList) -> UUIDList:
    request_data = profile_names

    request_header = {"Content-Type": "application/json"}

    r = requests.post(_get_uuids_url, json=request_data, headers=request_header)
    return r.json()


def _get_profiles(uuids: UUIDList):
    result = ProfileList()
    for i in uuids:
        url = re.sub(_replace_get_profiles_url_pattern, i["id"], _get_profiles_url)
        r = requests.get(url)
        result.append(r.json())
    return result


def _resolve_profiles(profiles: ProfileList):
    result = TextureList()
    for i in profiles:
        for j in i["properties"]:
            texture = json.loads(b64decode(j["value"]))
            result.append(texture)

    return result


def _resolve_texture(textures: TextureList):
    result = TextureUrlList()
    for i in textures:
        tmp_skin = None
        tmp_cape = None
        if "SKIN" in i["textures"]:
            tmp_skin = Url(name="skin", url=i["textures"]["SKIN"]["url"])
        if "CAPE" in i["textures"]:
            tmp_cape = Url(name="cape", url=i["textures"]["CAPE"]["url"])

        tmp = TextureUrls(
            skin_url=tmp_skin, cape_url=tmp_cape, profile_name=i["profileName"]
        )
        result.append(tmp)
    return result


def get_profile_microsoft(profile_names: NameList):
    uuids = _get_uuids(profile_names)
    profiles = _get_profiles(uuids)

    return profiles


def get_skin(profiles: ProfileList):
    textures = _resolve_profiles(profiles)
    urls = _resolve_texture(textures)

    return urls
