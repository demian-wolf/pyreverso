# Reverso-API

### What's this?
<i>This is a wrapper around Reverso's ([reverso.net](https://reverso.net)) API for Python.</i>

There is a very good website -- [Reverso](https://reverso.net). It's a very powerful and useful tool for those
people, who learn foreign languages. It consists of several sub-apps:
<ul>
<li><a href="https://context.reverso.net">Context</a> -- translation of words and most of complex phrases.
with usage examples.</li>
<li><a href="https://conjugator.reverso.net">Conjugator</a> -- a verb conjugator</li>
<li><a href="https://dictionary.reverso.net">Dictionary</a> -- a dictionary (both definitions and translation to other languages)</li>
<li><a href="https://reverso.net/spell-checker">Spell Checker</a> -- a spell checker.</li>
<li>and others</li>
</ul>

It also has a pretty good "Speak" feature for different languages ([Reverso Voice](https://voice.reverso.net/RestPronunciation.svc/help);
<a href="https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Heather22k?inputText=VGhpcyBpcyBhbiBleGFtcGxlIG9mIGEgdGV4dCwgc3Bva2VuIGJ5IFJldmVyc28gVm9pY2U=">here</a> is an example of spoken text).

Once upon a time I was writing a language-learning app, and wanted to include word translation with examples (as
in Reverso Context). But, unfortunately, I could not find a ready wrapper around this web-site's API. So I decided to create it
on my own.

### Features
Currently the wrapper supports Reverso Context API and Reverso Voice API.

### Docs
Docs are not ready yet; they'll be published soon. Every method of the code has docstrings, you can take a look
at them.

### Getting started

###### Installation
First, install the package with pip. Just type in the terminal/command-line:
```
pip install reverso-api
```

###### Creating a simple ReversoContextAPI-based program:
```python
import reverso_api
```

Now, let's get the translations of the word/phrase from English to Chinese and get first ten words' usage examples.

1. Create an instance of ReversoContextAPI:
```python
api = reverso_api.context.ReversoContextAPI(input("Enter the word/phrase to be translated... "),
                                            input("Enter the word/phrase that must be in the translation examples"),
                                            input("Enter the source language... "),
                                            input("Enter the target language... ")
                                            )
```

2. Let's get the translations:
```python
for source_word, translation, frequency, part_of_speech, inflected_forms in api.get_translations():
    print(source_word, "==" translation)
    print("Frequency (how many word usage examples contain this word):", frequency)
    print("Part of speech:", part_of_speech)
    if inflected_forms:
        print("Inflected forms:", ", ".join(inflected_forms))
    print()
```

3. And now let's get first ten translation examples:
```python
examples = api.get_translation_examples_pair_by_pair()
for _ in range(10):
    source, target = next(examples)
    print(source.text, "==", target.text)
```

4. Congratulations! You have created the first app that uses ReversoContextAPI.

###### Creating a simple ReversoVoice-based program:
TODO