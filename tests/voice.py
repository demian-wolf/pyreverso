import unittest
import contextlib

from reverso_api.voice import ReversoVoiceAPI, Voice, get_voices


def ask(what):
    while True:
        i = input("\n" + what + " [Y/N] ").upper()
        if i.startswith("Y"):
            return True
        elif i.startswith("N"):
            return False

class TestReversoVoiceAPI(unittest.TestCase):
    api = ReversoVoiceAPI("Hello, World!", "Heather22k")

    def test__get_voices(self):
        voices = get_voices()
        self.assertTrue(isinstance(voices, dict))
        for k, v in voices.items():
            self.assertTrue(isinstance(k, str))
            self.assertTrue(isinstance(v, list))
            for voice in v:
                self.assertTrue(isinstance(voice, Voice))              

    def test__mp3_data(self):
        voices = get_voices()
        for voice in (voices["US English"][0], "Heather22k"):
            self.api.voice = voice
            mp3_data = self.api.mp3_data
            self.assertTrue(isinstance(mp3_data, bytes))
            with open("data/voice/hello_world_us.mp3", "rb") as fp:
                self.assertEqual(fp.read(), mp3_data)

    def test__write_to_file(self):
        pass

    def test__say(self):
        voices = get_voices()
        try:
            with contextlib.redirect_stdout(None):
                import pygame
        except ImportError:
            print("\n.say(...) method cannot be checked without pygame. Install it first.")
            return
        for voice in [voices["US English"][0], "Heather22k"]:
            self.api.say(wait=True)
        self.assertTrue(ask("Have you heard the voice, played 2 times?"))
