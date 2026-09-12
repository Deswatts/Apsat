# Apsat  Copyright (C) 2026  Deswatts<Deswatts_Cre@outlook.com>
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.


class ProfileException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class ProfileHasNotCustomSkin(ProfileException):
    def __init__(self):
        super().__init__("The Profile dose not have any custom skin!")


class ProfileHasNotCustomCape(ProfileException):
    def __init__(self):
        super().__init__("The Profile dose not have any custom cape!")
