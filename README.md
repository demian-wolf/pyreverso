# Reverso-API

### What's this?
*This is a wrapper around Reverso's ([reverso.net](https://reverso.net)) API for Python.*

There is a very good website -- [Reverso](https://reverso.net). It's a very powerful and useful tool for those
people, who learn foreign languages. It consists of several sub-apps:
+ [Context](https://context.reverso.net) -- translation of words and most of complex phrases.
with usage examples.
+ [Conjugator](https://conjugator.reverso.net) -- a verb conjugator.
+ [Dictionary](https://dictionary.reverso.net) -- a dictionary (both definitions and translation to other languages).
+ [Spell Checker](https://reverso.net/spell-checker) -- a spell checker.
+ and others


It also has a pretty good "Speak" feature for different languages ([Reverso Voice](https://voice.reverso.net/RestPronunciation.svc/help);
[here](https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Heather22k?inputText=VGhpcyBpcyBhbiBleGFtcGxlIG9mIGEgdGV4dCwgc3Bva2VuIGJ5IFJldmVyc28gVm9pY2U=) is an example of spoken text).

Once upon a time I was writing a language-learning app, and wanted to include word translation with examples (as
in Reverso Context). But, unfortunately, I could not find a ready wrapper around this web-site's API. So I decided to
create it on my own.

### Features
Currently the wrapper supports Reverso Context API and Reverso Voice API.

### Docs
Docs are not ready yet; they will be published soon. Every method of the code has docstrings,
currently you can take a look at them. Also both reverso_api.context and reverso_api.voice
contain a sample usage example (after `if __name__ == "__main__"`); they are different from examples
below ("Getting started" section), and show more advanced features (such as surrounding highlighted
parts of words' usage examples in Context by *).

### Getting started

#### Installation
First, install the package with pip. Just type in the terminal/command-line:
```
pip install reverso-api
```

#### Creating a simple ReversoContextAPI-based program (mini, command-line version of Reverso Context):
1. Import the Reverso-API module:
    ```python
    from reverso_api.context import ReversoContextAPI
    ```

2. Create an instance of ReversoContextAPI:
    ```python
    api = ReversoContextAPI(
                            input("Enter the word/phrase to be translated... "),
                            input("Enter the word/phrase that must be in (target) word usage examples... "),
                            input("Enter the source language... "),
                            input("Enter the target language... ")
                            )
    ```

3. Let's get the translations:
    ```python
    for source_word, translation, frequency, part_of_speech, inflected_forms in api.get_translations():
        print(source_word, "==", translation)
        print("Frequency (how many word usage examples contain this word):", frequency)
        print("Part of speech:", part_of_speech if part_of_speech else "unknown")
        if inflected_forms:
            print("Inflected forms:", ", ".join(map(lambda form: str(form.translation), inflected_forms)))
        print()
    ```

4. And now let's get first ten translation examples:
    ```python
    examples = api.get_translation_examples_pair_by_pair()
    for _ in range(10):
        source, target = next(examples)
        print(source.text, "==", target.text)
    ```

5. Congratulations! You have created your first app that uses ReversoContextAPI!

#### Creating a simple ReversoVoiceAPI-based program ("Hello, World!" spoken by different people):
1. Import the Reverso-API module:
    ```python
    from reverso_api.voice import ReversoVoiceAPI
    ```

2. Create an instance of ReversoVoiceAPI:
    ```python
    api = ReversoVoiceAPI()
    ```

3. Let's find all the voices:
    ```python
    voices = api.get_available_voices()
    for voice in voices["US English"]:
        api.say("Hello, World!", voice, wait=True)
    ```

4. Congratulations! You have created your first app that uses ReversoVoiceAPI!