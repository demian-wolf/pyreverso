#!/usr/bin/env python

"""Reverso Voice (voice.reverso.net) API for Python"""

from collections import namedtuple, defaultdict
import contextlib
import base64
import json
import io

import requests


__all__ = ["ReversoVoiceAPI", "Voice"]

Voice = namedtuple("Voice", ("name", "language", "gender"))


class ReversoVoiceAPI:
    """Class for Reverso Voice API (https://voice.reverso.net/)

    Methods:
        get_available_voices()
        get_mp3_data(text, voice, speed=100)
        write_to_file(file, text, voice, speed=100)
        _write_to_fp(fp, text, voice, speed=100)
        say(text, voice, speed=100, wait=False)

    """

    def __init__(self):
        pass

    def get_available_voices(self):
        """Gets a list of available voices.

        Returns:
            A dict of available voices, where every key is a language name (e.g. "Arabic") and every value is a list
            of Voice namedtuples.

        """

        voices = defaultdict(list)
        for voice in json.loads(requests.get("https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetAvailableVoices").content)["Voices"]:
            language = voice["Language"]
            voices[language].append(Voice(voice["Name"], (int(voice["LangCode"]), language), voice["Gender"]))
        return dict(voices)

    def get_mp3_data(self, text, voice, speed=100):
        """Gets the spoken phrase as an MP3-data.

        Args:
             text: The text to be spoken
             voice: The voice which will speak the text
             speed: The speed of the voice

        Returns:
            A bytes-like object which contains the spoken phrase as an MP3-data.

        """

        if isinstance(voice, Voice):
            voice = voice.name

        return requests.get(
            "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName={}?voiceSpeed={}&inputText={}".format(
                voice, speed, base64.b64encode(text.encode()).decode())).content

    def write_to_file(self, file, text, voice, speed=100):
        """Writes the spoken phrase to an MP3 file. You can specify either filename-string or file-like object.
        If you are trying to pass another object as a file argument, TypeError is raised.

        Args:
            file: The output file (both strings with filenames and file-like objects are supported)
            text: The text to be spoken
            voice: The voice which will speak the text
            speed: The speed of the voice

        Returns:
            none

        Raises:
            TypeError: if not filename (string) or a file-like object is passed as a file argument.

        """

        if isinstance(file, str):
            with open(file, "wb") as fp:
                self._write_to_fp(fp, text, voice, speed)
            return
        if hasattr(file, "write"):
            self._write_to_fp(file, text, voice, speed)
            return
        raise TypeError("string or file-like object is required instead of {}".format(type(file)))

    def _write_to_fp(self, fp, text, voice, speed=100):
        """Writes the spoken phrase to a file-like object.

        Args:
            fp: The output file-like object
            text: The text to be spoken
            voice: The voice which will speak the text
            speed: The speed of the voice

        Returns:
            none

        """

        fp.write(self.get_mp3_data(text, voice, speed))

    def say(self, text, voice, speed=100, wait=False):
        """Speaks the given text. The difference from another similar methods is that this one PLAYS
        the sound (you can hear it if sound is enabled in your OS).

        Note:
            Pygame is necessary for this method to work! You should install it before calling this
            method, otherwise ImportError will be raised.

        Args:
            text: The text to be spoken
            voice: The voice which will speak the text
            speed: The speed of the voice
            wait: Tells whether it's necessary to wait till the text is fully spoken

        Returns:
            none

        Raises:
            ImportError: if Pygame is not installed

        """

        try:
            with contextlib.redirect_stdout(None):  # to remove "Hello from the pygame community..."
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
    from pprint import pprint
    import random

    print("Reverso.Voice API usage example")

    print()
    api = ReversoVoiceAPI()
    print("Available Voices:")
    voices = api.get_available_voices()
    pprint(voices)
    print()

    english_voice = random.choice(voices[random.choice(("Australian English",
                                                       "British",
                                                       "Indian English",
                                                       "US English"))])
    chinese_voice = random.choice(voices[random.choice(("Mandarin Chinese",))])

    print("And now let's speak something. English voice is {} and Chinese voice is {}".format(english_voice,
                                                                                              chinese_voice))
    for data in [("The phrase", english_voice),
                 ("能让我来照顾你的小猫咪吗？", chinese_voice, 85),
                 ("is translated from Chinese like", english_voice),
                 ("Can I adopt your little kitten?", english_voice)
                 ]:
        print(data[0])
        api.say(*data, wait=True)
