# Apsat  Copyright (C) 2026  Deswatts<Deswatts_Cre@outlook.com>
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.


from typing import TypedDict


class SkinMetadata(TypedDict):
    model: str | None


class SkinObject(TypedDict):
    url: str
    model: SkinMetadata | None


class CapeObject(TypedDict):
    url: str


class TextureDict(TypedDict):
    SKIN: SkinObject | None
    CAPE: CapeObject | None


class TextureObject(TypedDict):
    timestamp: int
    profileId: str
    profileName: str
    signatureRequired: bool | None
    textures: TextureDict


class ProfileProperties(list):
    name: str
    signature: str | None
    value: str


class Profile(TypedDict):
    id: str
    name: str
    legacy: bool | None
    properties: ProfileProperties


class Url(TypedDict):
    name: str
    url: str


class UUIDList(list):
    uuids: str


class NameList(list):
    names: str


class ProfileList(list):
    profiles: Profile


class TextureList(list):
    texture_objects: TextureObject


class TextureUrls(TypedDict):
    skin_url: Url | None
    cape_url: Url | None
    profile_name: str


class TextureUrlList(list):
    urls: TextureUrls


class ProfileType(int):
    type: str

    def __new__(cls, mode):
        cls.type = cls.to_binary(mode)
        cls.type = "0" * (5 - len(cls.type)) + cls.type
        return cls

    @staticmethod
    def to_binary(mode: str):
        if int(mode) // 2 == 0:
            return str(int(mode) % 2)
        else:
            tmp = ProfileType.to_binary(str(int(mode) // 2))
            return tmp + str(int(mode) % 2)
