"""Reverso Voice (voice.reverso.net) API for Python"""

from collections import namedtuple, defaultdict
import contextlib
import base64
import json
import io

import requests


__all__ = ["ReversoVoiceAPI", "Voice"]

BASE_URL = "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/"

Voice = namedtuple("Voice", ("name", "language", "gender"))


class ReversoVoiceAPI:
    """Class for Reverso Voice API (https://voice.reverso.net/)

    Attributes:
        voices

    Methods:
        get_mp3_data(text, voice, speed=100)
        write_to_file(file, text, voice, speed=100)
        say(text, voice, speed=100, wait=False)

    """

    def __init__(self):
        _voices = defaultdict(list)
        self._voice_names = []
        for voice in json.loads(requests.get(BASE_URL + "GetAvailableVoices").content)["Voices"]:
            language_name = voice["Language"]
            _voices[language_name].append(
                Voice(voice["Name"], (int(voice["LangCode"]), language_name), voice["Gender"]))
            self._voice_names.append(voice["Name"])
        self.voices = dict(_voices)

    def get_mp3_data(self, text, voice, speed=100):
        """Gets the spoken phrase as an MP3-data.

        Args:
             text: The text to be spoken
             voice: The voice which will speak the text (can be either str or a Voice namedtuple)
             speed: The speed of the voice

        Returns:
            A bytes-like object which contains the spoken phrase as an MP3-data.

        """

        if isinstance(voice, Voice):
            voice = voice.name

        if voice not in self._voice_names:
            raise ValueError("the given voice is invalid")

        return requests.get(BASE_URL + "GetVoiceStream/voiceName={}?voiceSpeed={}&inputText={}".format(
            voice, speed, base64.b64encode(text.encode()).decode())).content

    def write_to_file(self, file, text, voice, speed=100):
        """Writes the spoken phrase to an MP3 file. You can specify either a filename-string or a file-like object.
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
                fp.write(self.get_mp3_data(text, voice, speed))
            return
        if hasattr(file, "write"):
            file.write(self.get_mp3_data(text, voice, speed))
            return
        raise TypeError("string or file-like object is required instead of {}".format(type(file)))

    def say(self, text, voice, speed=100, wait=False):
        """Reads the given text aloud. The difference from other methods is that this one PLAYS
        the sound (you can hear it if sound is enabled in your OS and pygame is installed).

        Note:
            Pygame is necessary for this method to work! You should install it before calling this
            method, otherwise ImportError will be raised.

        Args:
            text: The text to be spoken
            voice: The voice which will speak the text
            speed: The speed of the voice
            wait: Tells whether it's necessary to wait until the text is fully spoken

        Returns:
            none

        Raises:
            ImportError: if Pygame is not installed

        """

        try:
            with contextlib.redirect_stdout(None):  # to remove the "Hello from the pygame community..." message
                import pygame
        except ImportError:
            raise ImportError("pygame is required for playing mp3 files, so you should install it first")

        pygame.mixer.init()
        with io.BytesIO() as fp:
            fp.write(self.get_mp3_data(text, voice, speed))
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            if wait:
                while pygame.mixer.music.get_busy():
                    pygame.time.delay(100)
