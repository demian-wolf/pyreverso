"""Reverso Voice (voice.reverso.net) API for Python"""

from collections import namedtuple, defaultdict
import contextlib
import base64
import json
import io

import requests


__all__ = ["ReversoVoiceAPI", "Voice", "get_voices"]

BASE_URL = "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/"

Voice = namedtuple("Voice", ("name", "language", "gender"))

def get_voices():
    _voices = defaultdict(list)
    for voice in json.loads(requests.get(BASE_URL + "GetAvailableVoices").content)["Voices"]:
        language_name = voice["Language"]
        _voices[language_name].append(
            Voice(voice["Name"], (int(voice["LangCode"]), language_name), voice["Gender"]))
    return dict(_voices)

class ReversoVoiceAPI:
    """Class for Reverso Voice API (https://voice.reverso.net/)

    Attributes:
        text
        voice
        speed
        mp3_data

    Methods:
        write_to_file(file)
        say(wait=False)

    """

    def __init__(self, text, voice, speed=100):
        self.__voice_names = [voice.name
                               for _, voices_list in get_voices().items()
                               for voice in voices_list]
        self.__text, self.__voice, self.__speed = None, None, None
        self.text, self.voice, self.speed = text, voice, speed
    
    @property
    def text(self):
        return self.__text

    @property
    def voice(self):
        return self.__voice

    @property
    def speed(self):
        return self.__speed

    @property
    def mp3_data(self):
        if self.__info_modified:
            self.__mp3_data = requests.get(BASE_URL + "GetVoiceStream/voiceName={}?voiceSpeed={}&inputText={}".format(self.voice, self.speed, base64.b64encode(self.text.encode()).decode())).content
            self.__info_modified = False
        return self.__mp3_data
    
    @text.setter
    def text(self, value):
        assert isinstance(value, str), "text must be a string"
        self.__text = value
        self.__info_modified = True

    @voice.setter
    def voice(self, value):
        if isinstance(value, Voice):
            value = value.name
        assert value in self.__voice_names, "invalid voice"
        self.__voice = value
        self.__info_modified = True

    @speed.setter
    def speed(self, value):
        assert isinstance(value, int), "speed must be an integer"
        assert 30 <= value <= 300, "speed must be 30 <= speed <= 300"
        self.__speed = value
        self.__info_modified = True
        

    def write_to_file(self, file):
        """Writes the spoken phrase to an MP3 file. You can specify either a filename-string or a file-like object.
        If you are trying to pass another object as a file argument, TypeError is raised.

        Args:
            file: The output file (both strings with filenames and file-like objects are supported)

        Returns:
            none

        Raises:
            TypeError: if not filename (string) or a file-like object is passed as a file argument.

        """

        if isinstance(file, str):
            with open(file, "wb") as fp:
                fp.write(self.mp3_data)
            return
        if hasattr(file, "write"):
            file.write(self.mp3_data)
            return
        raise TypeError("string or file-like object is required instead of {}".format(type(file)))

    def say(self, wait=False):
        """Reads the given text aloud. The difference from other methods is that this one PLAYS
        the sound (you can hear it if sound is enabled in your OS and pygame is installed).

        Note:
            Pygame is necessary for this method to work! You should install it before calling this
            method, otherwise ImportError will be raised.

        Args:
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
            self.write_to_file(fp)
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            if wait:
                while pygame.mixer.music.get_busy():
                    pygame.time.delay(100)
