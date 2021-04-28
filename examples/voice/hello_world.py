"""'Hello, World!' sentence said in all available 'US English' voices.

Note: pygame is required for this example to work."""


from reverso_api.voice import ReversoVoiceAPI


api = ReversoVoiceAPI()
for voice in api.voices["US English"]:
    api.say("Hello, World!", voice, wait=True)