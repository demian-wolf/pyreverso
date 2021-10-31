"""'Hello, World!' sentence said in all available 'US English' voices.

Note: pygame is required for this example to work."""


from reverso_api import ReversoVoiceAPI


api = ReversoVoiceAPI(text="Hello, World!", voice="Heather22k")

for voice in api.voices["US English"]:
    api.say("Hello, World!", voice, wait=True)