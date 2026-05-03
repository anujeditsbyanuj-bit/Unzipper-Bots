import logging
import asyncio
from json import loads

USER_LANG = {}
STRINGS = {}


def update_languages_cache():
    from unzipper.database.language import get_user_languages

    async def _iter_and_update():
        async for doc in get_user_languages():
            USER_LANG[doc["_id"]] = doc["lang"]

    # SAFE RUN (Render compatible)
    asyncio.create_task(_iter_and_update())


def update_text_strings():
    def _read_json(file, as_items=False):
        with open(file, encoding="utf-8") as f:
            return loads(f.read()).items() if as_items else loads(f.read())

    subfolders = _read_json("unzipper/localization/languages.json", True)

    for lcode, fnm in subfolders:
        str_list = _read_json(f"unzipper/localization/{lcode}/messages.json")
        btn_strs = _read_json("unzipper/localization/defaults/buttons.json")

        STRINGS[lcode] = str_list
        STRINGS["buttons"] = btn_strs


def update_cache():
    logging.info(" >> Updating text strings cache...")
    update_text_strings()

    logging.info(" >> Updating language cache...")
    update_languages_cache()
