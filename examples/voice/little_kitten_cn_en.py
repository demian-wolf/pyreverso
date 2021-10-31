"""'Can I adopt your little kitten?' sentence spoken in Chinese and in English with random chosen voices.

Note: pygame is required for this example to work."""

from reverso_api.voice import ReversoVoiceAPI
from pprint import pprint
import random


print("Reverso.voice API usage example")

print()
api = ReversoVoiceAPI()
print("Available Voices:")
voices = api.voices
pprint(voices)
print()

english_voice = random.choice(voices[random.choice(("Australian English",
                                                    "British",
                                                    "Indian English",
                                                    "US English"))])
chinese_voice = random.choice(voices[random.choice(("Mandarin Chinese",))])

print("And now let's say something. English voice is {} and Chinese voice is {}".format(english_voice,
                                                                                          chinese_voice))
for data in [("The phrase", english_voice),
             ("能让我来照顾你的小猫咪吗？", chinese_voice, 85),
             ("is translated from Chinese like", english_voice),
             ("Can I adopt your little kitten?", english_voice)
             ]:
    print(data[0])
    api.say(*data, wait=True)