#!/usr/bin/env python

from collections import namedtuple
import json

import requests


Voice = namedtuple("Voice", ("name", "language", "gender"))


class ReversoVoiceAPI:

    def __init__(self):
        pass

    def get_available_voices(self):
        voices = []
        for voice in json.loads(requests.get(
                "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetAvailableVoices").content)["Voices"]:
            voices.append(Voice(voice["Name"], (int(voice["LangCode"]), voice["Language"]), voice["Gender"]))
        return voices


# A simple usage example
if __name__ == "__main__":
    api = ReversoVoiceAPI()
    for voice in api.get_available_voices():
        print(voice)
