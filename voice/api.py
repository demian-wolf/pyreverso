#!/usr/bin/env python

from collections import namedtuple
import contextlib
import base64
import json
import io

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

    def get_mp3_data(self, text, voice, speed=100):
        return requests.get(
            "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName={}?voiceSpeed={}&inputText={}".format(
                voice, speed, base64.b64encode(text.encode()).decode())).content

    def write_to_file(self, file, text, voice, speed=100):
        if isinstance(file, str):
            with open(file, "wb") as fp:
                self._write_to_fp(fp, text, voice, speed)
            return
        if hasattr(file, "write"):
            self._write_to_fp(file, text, voice, speed)
            return
        raise TypeError("string or file-like object is required instead of {}".format(type(file)))

    def _write_to_fp(self, fp, text, voice, speed=100):
        fp.write(self.get_mp3_data(text, voice, speed))

    def say(self, text, voice, speed=100, wait=False):
        try:
            with contextlib.redirect_stdout(None):
                import pygame
        except ImportError:
            raise ImportError("pygame is required for playing mp3 files, so you should install it first")
        pygame.mixer.init()
        fp = io.BytesIO()
        self._write_to_fp(fp, text, voice, speed)
        fp.seek(0)
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        if wait:
            while pygame.mixer.music.get_busy():
                pygame.time.delay(100)


# A simple usage example
if __name__ == "__main__":
    api = ReversoVoiceAPI()
    print("Available Voices:", api.get_available_voices())

    print("And now let's speak something!")
    for data in [("This phrase", "Heather22k"),
                 ("能让我来照顾你的小猫咪吗？", "Lulu22k", 85),
                 ("is translated from Chinese like", "Heather22k"),
                 ("Can I adopt your little kitten?", "Heather22k")
                 ]:
        api.say(*data, wait=True)

