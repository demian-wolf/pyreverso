import unittest
import contextlib

from reverso_api.voice import ReversoVoiceAPI, Voice


def ask(what):
    while True:
        i = input("\n" + what + " [Y/N] ").upper()
        if i.startswith("Y"):
            return True
        elif i.startswith("N"):
            return False

class TestReversoVoiceAPI(unittest.TestCase):
    api = ReversoVoiceAPI()

    def test__voices(self):
        voices = self.api.voices
        self.assertTrue(isinstance(voices, dict))
        for k, v in voices.items():
            self.assertTrue(isinstance(k, str))
            self.assertTrue(isinstance(v, list))
            for voice in v:
                self.assertTrue(isinstance(voice, Voice))              

    def test__get_mp3_data(self):
        self.assertRaises(ValueError, self.api.get_mp3_data, "Hello, World!", "a definitely invalid voice", 100)
        for voice in [self.api.voices["US English"][0], "Heather22k"]:
            mp3_data = self.api.get_mp3_data("Hello, World!", voice, 100)
            self.assertTrue(isinstance(mp3_data, bytes))
            with open("data/voice/hello_world_us.mp3", "rb") as fp:
                self.assertEqual(fp.read(), mp3_data)

    def test__write_to_file(self):
        pass

    def test__say(self):
        try:
            with contextlib.redirect_stdout(None):
                import pygame
        except ImportError:
            print("\n.say(...) method cannot be checked without pygame. Install it first.")
            return
        for voice in [self.api.voices["US English"][0], "Heather22k"]:
            self.api.say("Hello, World!", voice, 100, True)
        self.assertTrue(ask("Have you heard the voice, played 2 times?"))